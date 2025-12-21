"""
DailyMind AI Backend API
========================
Günlük yazma uygulaması için FastAPI backend servisi.
- NLP tabanlı duygu analizi
- Groq AI ile kişiselleştirilmiş içgörüler
- Supabase auth ve veritabanı entegrasyonu
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from nlp_pipeline import analyze_text

load_dotenv()

# Supabase Ayarları
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase bağlantı hatası: {e}")
    supabase = None

# Groq API Key (YENİ - ÜCRETSİZ!)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ UYARI: GROQ_API_KEY eksik.")

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

def prepare_features_single(analysis_json: Dict, created_at_str: str) -> pd.DataFrame:
    """
    NLP analiz sonucunu ML modeli için feature vektörüne dönüştürür.
    
    Args:
        analysis_json: NLP pipeline'dan gelen analiz sonucu
        created_at_str: Giriş tarihi (ISO format)
    
    Returns:
        DataFrame: Scaled ve encoded feature vektörü
    """
    created_at = pd.to_datetime(created_at_str)
    topics = analysis_json.get('topics', [])
    metrics = analysis_json.get('metrics', {'kelime_sayisi': 0, 'karakter_sayisi': 0})
    entities = analysis_json.get('entities', [])
    
    # Sentiment skoru düzeltmesi (negative için negatif değer)
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

    # Temporal features
    row['saat'] = created_at.hour
    row['hafta_sonu'] = 1 if created_at.dayofweek >= 5 else 0
    for d in range(7): 
        row[f'gun_{d}'] = 1 if created_at.dayofweek == d else 0
        
    hour = created_at.hour
    time_period = 'gece' if 0 <= hour < 6 else 'sabah' if 6 <= hour < 12 else 'ogle' if 12 <= hour < 18 else 'aksam'
    for tp in ['gece', 'sabah', 'ogle', 'aksam']: 
        row[f'zaman_{tp}'] = 1 if time_period == tp else 0

    # Topic one-hot encoding
    KONU_LISTESI = [
        "İş ve Kariyer", "Eğitim ve Okul", "Sosyal İlişkiler", "Aile",
        "Sağlık", "Finans ve Para", "Teknoloji", "Kişisel Gelişim", "Genel Günlük"
    ]
    for konu in KONU_LISTESI:
        key = f"konu_{konu.replace(' ', '_').replace('İ', 'I').lower()}"
        row[key] = 1 if konu in topics else 0

    # Entity counts
    entity_counts = {'PER': 0, 'ORG': 0, 'LOC': 0}
    for e in entities:
        if e['varlik'] in entity_counts: 
            entity_counts[e['varlik']] += 1
    for etype in ['PER', 'ORG', 'LOC']: 
        row[f'varlik_sayisi_{etype}'] = entity_counts[etype]

    df = pd.DataFrame([row])
    
    # Model feature alignment
    for col in MODEL_FEATURES:
        if col not in df.columns: 
            df[col] = 0
    df = df[MODEL_FEATURES]
    
    # Feature scaling
    if SCALER:
        cols_to_scale = ['kelime_sayisi', 'karakter_sayisi', 'duygu_skoru', 'varlik_toplam_sayi']
        df[cols_to_scale] = SCALER.transform(df[cols_to_scale])
        
    return df

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserAuth(BaseModel):
    email: EmailStr
    password: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Supabase JWT token'ı doğrular ve kullanıcı bilgisini döner."""
    try:
        response = supabase.auth.get_user(token)
        if not response or not response.user:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        print(f"✅ Authenticated User ID: {response.user.id}")
        return response.user
    except Exception as e:
        print(f"❌ Auth Error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Yetkilendirme hatası: {str(e)}")

class Girdi(BaseModel):
    metin: str

@app.get("/")
def root():
    return {"status": "Running", "model": "Mood Regressor"}

@app.post("/auth/signup")
def signup(user: UserAuth):
    """Yeni kullanıcı kaydı oluşturur."""
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"msg": "Kayıt başarılı", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(user: UserAuth):
    """Kullanıcı girişi yapar ve JWT token döner."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Giriş başarısız. Email veya şifre hatalı.")

@app.post("/entries")
def create_entry(girdi: Girdi, user: Any = Depends(get_current_user)):
    """
    Yeni günlük girişi oluşturur ve NLP analizi yapar.
    
    Flow:
    1. Metni NLP pipeline'a gönder
    2. Analiz sonucunu veritabanına kaydet
    3. User ID ile ilişkilendir
    """
    if not supabase: 
        raise HTTPException(500, "DB Bağlantı Hatası")
    
    try:
        print(f"Gelen metin: {girdi.metin[:30]}...")
        print(f"User ID: {user.id}")
        
        analiz = analyze_text(girdi.metin)
        if analiz.get("hata"): 
            raise HTTPException(500, analiz["hata"])

        data, _ = supabase.table('gunluk_girisler').insert({
            "metin": girdi.metin,
            "analiz_sonucu": analiz,
            "user_id": str(user.id)
        }).execute()
        
        print(f"✅ Entry created: {data[1][0]['id']}")
        return {"status": "success", "data": data[1][0]}
    except Exception as e:
        print(f"❌ Insert Error: {str(e)}")
        raise HTTPException(500, str(e))

@app.get("/entries")
def get_entries(limit: int = 50, user: Any = Depends(get_current_user)):
    """Kullanıcının günlüklerini tarih sırasına göre getirir."""
    if not supabase: 
        raise HTTPException(500, "DB Hatası")
    
    try:
        data, _ = supabase.table("gunluk_girisler")\
            .select("*")\
            .eq("user_id", user.id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return data[1]
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/predict-mood/{entry_id}")
def predict_mood(entry_id: int, user: Any = Depends(get_current_user)):
    """
    Belirli bir günlük girişi için ML tabanlı mood skoru tahmin eder.
    
    Returns:
        mood_score: 1.0-5.0 arası skor
        emoji: Skorla eşleşen emoji
        message: Açıklayıcı mesaj
    """
    if not MOOD_MODEL: 
        raise HTTPException(503, "Model Yüklenemedi")
    
    try:
        data, _ = supabase.table("gunluk_girisler")\
            .select("*")\
            .eq("id", entry_id)\
            .eq("user_id", user.id)\
            .execute()
            
        if not data[1]: 
            raise HTTPException(404, "Günlük bulunamadı veya erişim yetkiniz yok")
        
        entry = data[1][0]
        features = prepare_features_single(entry['analiz_sonucu'], entry['created_at'])
        prediction = MOOD_MODEL.predict(features)[0]
        mood_score = max(1.0, min(5.0, round(prediction, 1)))
        
        # Mood kategorileri
        if mood_score >= 4.5: 
            emoji, msg = "🤩", "Harika bir gün geçirmişsin!"
        elif mood_score >= 3.5: 
            emoji, msg = "😊", "Gayet olumlu ve keyifli."
        elif mood_score >= 2.5: 
            emoji, msg = "😐", "Rutin bir gün."
        elif mood_score >= 1.5: 
            emoji, msg = "😔", "Biraz zorlu olmuş."
        else: 
            emoji, msg = "😫", "Çok stresli bir gün, kendine dikkat et."

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

def get_ai_advice(topic: str, mood_score: float, entries_text: List[str]) -> str:
    """
    Groq API (Llama 3.1) kullanarak kişiselleştirilmiş psikolojik tavsiye üretir.
    
    Args:
        topic: Hedef konu (örn: "Sağlık", "İş ve Kariyer")
        mood_score: 1-5 arası mood puanı
        entries_text: Son günlük metinleri
    
    Returns:
        str: AI tavsiyesi veya fallback mesajı
    
    Fallback Stratejisi:
    - Groq API başarısız olursa mood_score'a göre önceden tanımlı mesajlar döner
    """
    durum = "olumlu/mutlu" if mood_score > 3.0 else "olumsuz/stresli"
    combined_texts = "\n".join([f"- {text[:150]}..." for text in entries_text[:3]])
    
    prompt = f"""Sen empatik bir psikoloğusun. Kullanıcıya kısa ve samimi tavsiye ver.

Konu: {topic}
Ruh Hali: {mood_score:.1f}/5 ({durum})

Son günlükler:
{combined_texts}

Kullanıcıya 1-2 cümlelik uygulanabilir tavsiye ver."""

    # Groq API çağrısı
    if GROQ_API_KEY:
        try:
            print(f"🚀 Groq API (Llama 3.1) deneniyor... Konu: {topic}")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "Sen empatik bir psikoloğusun. Kısa ve samimi tavsiyeler veriyorsun."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"].strip()
                if result and len(result) > 20:
                    print(f"✅ Groq başarılı: {result[:60]}...")
                    return result
            else:
                print(f"⚠️ Groq hatası: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Groq bağlantı hatası: {e}")
    else:
        print("⚠️ GROQ_API_KEY bulunamadı!")
    
    # Fallback mesajları (mood_score bazlı)
    print("⚠️ AI kullanılamıyor, akıllı fallback mesajı döndürülüyor.")
    
    if mood_score < 2.5:
        return f"'{topic}' konusu seni son günlerde yoruyor gibi görünüyor (Puan: {mood_score:.1f}/5). Kendine biraz zaman ayır ve bu konuda destek almayı düşünebilirsin."
    elif mood_score < 3.5:
        return f"'{topic}' konusunda dengeli görünüyorsun (Puan: {mood_score:.1f}/5). Küçük iyileştirmeler yaparak daha iyi hissedebilirsin."
    else:
        return f"'{topic}' konusunda harika gidiyorsun! (Puan: {mood_score:.1f}/5). Bu pozitif enerjiyi korumaya devam et."

@app.get("/insights")
def generate_insights(user: Any = Depends(get_current_user)):
    """
    Kullanıcının günlüklerini analiz ederek AI destekli içgörü üretir.
    
    Flow:
    1. Cache kontrolü (7 gün) - Gereksiz AI çağrısı önleme
    2. Günlükleri çek ve topic bazlı mood analizi yap
    3. En iyi/kötü konuyu belirle
    4. Groq AI'dan tavsiye al
    5. Sonucu cache'e kaydet
    
    Returns:
        insight: AI tavsiyesi
        related_topic: İlgili konu
        trend: "positive" | "negative" | "neutral"
        source: "cache" | "new_gen"
    """
    if not supabase:
        return {"insight": "Veritabanı hatası.", "related_topic": None, "trend": "neutral"}

    # Cache kontrolü (7 günlük)
    yedi_gun_once = (datetime.utcnow() - timedelta(days=7)).isoformat()
    
    try:
        existing_insight, _ = supabase.table("user_insights")\
            .select("*")\
            .eq("user_id", user.id)\
            .gte("created_at", yedi_gun_once)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        if existing_insight[1]:
            print("🔄 Cache'den veri getirildi (7 gün içinde).")
            cached_data = existing_insight[1][0]
            return {
                "insight": cached_data["insight_text"],
                "related_topic": cached_data["related_topic"],
                "trend": cached_data["trend"],
                "source": "cache"
            }
    except Exception as e:
        print(f"Cache kontrol hatası: {e}")

    # Yeni analiz başlat
    print(f"🔍 Yeni analiz başlatılıyor... User: {user.id}")
    
    try:
        data, _ = supabase.table("gunluk_girisler")\
            .select("*")\
            .eq("user_id", user.id)\
            .order("created_at", desc=True)\
            .limit(50)\
            .execute()
        
        entries = data[1]
        print(f"📚 {len(entries)} günlük bulundu.")
        
        if len(entries) < 3:
            return {
                "insight": "Henüz yeterli veri yok, yazmaya devam et! 📝", 
                "related_topic": None, 
                "trend": "neutral", 
                "source": "new_gen"
            }

        # Topic bazlı mood agregasyonu
        topic_moods = {} 
        topic_entries_text = {}

        for entry in entries:
            features = prepare_features_single(entry['analiz_sonucu'], entry['created_at'])
            predicted_mood = MOOD_MODEL.predict(features)[0] if MOOD_MODEL else 3.0
            
            topics = entry['analiz_sonucu'].get('topics', [])
            for topic in topics:
                if topic not in topic_moods:
                    topic_moods[topic] = []
                    topic_entries_text[topic] = []
                
                topic_moods[topic].append(predicted_mood)
                topic_entries_text[topic].append(entry['metin'])

        # Ortalama mood hesaplama
        avg_moods = []
        for topic, scores in topic_moods.items():
            if len(scores) >= 2:
                avg = sum(scores) / len(scores)
                avg_moods.append((topic, avg))
        
        if not avg_moods:
            return {
                "insight": "Veri analizi yapılıyor...", 
                "related_topic": None, 
                "trend": "neutral", 
                "source": "new_gen"
            }

        # En iyi ve en kötü konuyu bul
        avg_moods.sort(key=lambda x: x[1], reverse=True) 
        best_topic, best_score = avg_moods[0]
        worst_topic, worst_score = avg_moods[-1]
        
        print(f"📊 En iyi: {best_topic} ({best_score:.1f}), En kötü: {worst_topic} ({worst_score:.1f})")

        # Hedef konu seçimi (kötü < 2.5 ise ona odaklan)
        if worst_score < 2.5:
            target_topic = worst_topic
            target_score = worst_score
            trend = "negative"
        else:
            target_topic = best_topic
            target_score = best_score
            trend = "positive"

        # AI tavsiyesi al
        relevant_texts = topic_entries_text[target_topic][:5]
        print(f"🎯 Hedef konu: {target_topic}, Puan: {target_score:.1f}")
        
        final_insight = get_ai_advice(target_topic, target_score, relevant_texts)

        # Cache'e kaydet
        try:
            supabase.table("user_insights").insert({
                "user_id": str(user.id),
                "insight_text": final_insight,
                "related_topic": target_topic,
                "trend": trend
            }).execute()
            print("💾 İçgörü kaydedildi.")
        except Exception as e:
            print(f"Cache kayıt hatası: {e}")

        return {
            "insight": final_insight,
            "related_topic": target_topic,
            "trend": trend,
            "source": "new_gen"
        }

    except Exception as e:
        print(f"❌ Insight Hatası: {e}")
        import traceback
        traceback.print_exc()
        return {
            "insight": "İçgörüler şu an oluşturulamıyor.", 
            "related_topic": None, 
            "trend": "neutral", 
            "source": "error"
        }