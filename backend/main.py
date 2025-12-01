# main.py (FİNAL - DÜZELTİLMİŞ SÜRÜM)

import os
import json
import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# NLP Pipeline
from nlp_pipeline import analyze_text

# .env yükle
load_dotenv()

# Supabase Ayarları
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase bağlantı hatası: {e}")
    supabase = None

# --- MODELLERİ YÜKLE ---
print("🧠 Yapay Zeka Modelleri yükleniyor...")
MOOD_MODEL = None
SCALER = None
MODEL_FEATURES = []

try:
    with open('mood_regressor.pkl', 'rb') as f:
        model_data = pickle.load(f)
        MOOD_MODEL = model_data['model']
        MODEL_FEATURES = model_data['features']
    
    with open('scaler.pkl', 'rb') as f:
        SCALER = pickle.load(f)
        
    print("✅ Mood Regressor (v2) başarıyla yüklendi!")
except FileNotFoundError:
    print("⚠️ UYARI: .pkl dosyaları eksik. Tahmin yapılamaz.")

app = FastAPI(title="DailyMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- YARDIMCI FONKSİYON ---
def prepare_features_single(analysis_json: Dict, created_at_str: str) -> pd.DataFrame:
    """API'den gelen veriyi, modelin eğitimde gördüğü formata birebir çevirir."""
    created_at = pd.to_datetime(created_at_str)
    topics = analysis_json.get('topics', [])
    metrics = analysis_json.get('metrics', {'kelime_sayisi': 0, 'karakter_sayisi': 0})
    entities = analysis_json.get('entities', [])
    
    # Skor Düzeltmesi
    raw_score = analysis_json.get('sentiment', {}).get('skor', 0)
    sentiment_label = analysis_json.get('sentiment', {}).get('duygu', 'neutral')
    
    if sentiment_label == 'negative':
        final_score = raw_score * -1
    elif sentiment_label == 'neutral':
        final_score = 0
    else:
        final_score = raw_score

    row = {}
    row['kelime_sayisi'] = metrics.get('kelime_sayisi', 0)
    row['karakter_sayisi'] = metrics.get('karakter_sayisi', 0)
    row['duygu_skoru'] = final_score
    row['varlik_toplam_sayi'] = len(entities)

    row['saat'] = created_at.hour
    row['hafta_sonu'] = 1 if created_at.dayofweek >= 5 else 0
    for d in range(7): row[f'gun_{d}'] = 1 if created_at.dayofweek == d else 0
        
    hour = created_at.hour
    time_period = 'gece' if 0 <= hour < 6 else 'sabah' if 6 <= hour < 12 else 'ogle' if 12 <= hour < 18 else 'aksam'
    for tp in ['gece', 'sabah', 'ogle', 'aksam']: row[f'zaman_{tp}'] = 1 if time_period == tp else 0

    KONU_LISTESI = [
        "İş ve Kariyer", "Eğitim ve Okul", "Sosyal İlişkiler", "Aile",
        "Sağlık", "Finans ve Para", "Teknoloji", "Kişisel Gelişim", "Genel Günlük"
    ]
    for konu in KONU_LISTESI:
        key = f"konu_{konu.replace(' ', '_').replace('İ', 'I').lower()}"
        row[key] = 1 if konu in topics else 0

    entity_counts = {'PER': 0, 'ORG': 0, 'LOC': 0}
    for e in entities:
        if e['varlik'] in entity_counts: entity_counts[e['varlik']] += 1
    for etype in ['PER', 'ORG', 'LOC']: row[f'varlik_sayisi_{etype}'] = entity_counts[etype]

    df = pd.DataFrame([row])
    for col in MODEL_FEATURES:
        if col not in df.columns: df[col] = 0
    
    df = df[MODEL_FEATURES]
    
    if SCALER:
        cols_to_scale = ['kelime_sayisi', 'karakter_sayisi', 'duygu_skoru', 'varlik_toplam_sayi']
        df[cols_to_scale] = SCALER.transform(df[cols_to_scale])
        
    return df

# --- ENDPOINTLER ---

class Girdi(BaseModel):
    metin: str

@app.get("/")
def root():
    return {"status": "Running", "model": "Mood Regressor"}

# 1. GÜNLÜK EKLEME (POST)
@app.post("/entries")
def create_entry(girdi: Girdi):
    if not supabase: raise HTTPException(500, "DB Bağlantı Hatası")
    try:
        print(f"Gelen metin: {girdi.metin[:30]}...")
        analiz = analyze_text(girdi.metin)
        if analiz.get("hata"): raise HTTPException(500, analiz["hata"])

        data, _ = supabase.table('gunluk_girisler').insert({
            "metin": girdi.metin,
            "analiz_sonucu": analiz
        }).execute()
        
        return {"status": "success", "data": data[1][0]}
    except Exception as e:
        raise HTTPException(500, str(e))

# 2. GÜNLÜKLERİ LİSTELEME (GET) - EKSİK OLAN KISIM BUYDU!
@app.get("/entries")
def get_entries(limit: int = 50):
    """Geçmiş günlük kayıtlarını listeler"""
    if not supabase: raise HTTPException(500, "DB Hatası")
    try:
        # Tarihe göre tersten sırala (en yeni en üstte)
        data, _ = supabase.table("gunluk_girisler")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return data[1]
    except Exception as e:
        raise HTTPException(500, str(e))

# 3. MOOD TAHMİNİ (GET)
@app.get("/predict-mood/{entry_id}")
def predict_mood(entry_id: int):
    if not MOOD_MODEL: raise HTTPException(503, "Model Yüklenemedi")
    
    try:
        data, _ = supabase.table("gunluk_girisler").select("*").eq("id", entry_id).execute()
        if not data[1]: raise HTTPException(404, "Günlük bulunamadı")
        entry = data[1][0]
        
        features = prepare_features_single(entry['analiz_sonucu'], entry['created_at'])
        prediction = MOOD_MODEL.predict(features)[0]
        
        mood_score = max(1.0, min(5.0, round(prediction, 1)))
        
        if mood_score >= 4.5: emoji, msg = "🤩", "Harika bir gün geçirmişsin!"
        elif mood_score >= 3.5: emoji, msg = "😊", "Gayet olumlu ve keyifli."
        elif mood_score >= 2.5: emoji, msg = "😐", "Rutin bir gün."
        elif mood_score >= 1.5: emoji, msg = "😔", "Biraz zorlu olmuş."
        else: emoji, msg = "😫", "Çok stresli bir gün, kendine dikkat et."

        return {
            "entry_id": entry_id,
            "ai_prediction": {
                "mood_score": mood_score,
                "emoji": emoji,
                "message": msg
            }
        }
        
    except Exception as e:
        print(f"Hata: {e}")
        raise HTTPException(500, f"Tahmin hatası: {str(e)}")