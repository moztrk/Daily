# prepare_data.py (ZEKİ SİMÜLASYON SÜRÜMÜ)

import os
import pandas as pd
import json
import pickle
import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Konfigürasyon
MIN_REQUIRED_SAMPLES = 200
KONU_LISTESI = [
    "İş ve Kariyer", "Eğitim ve Okul", "Sosyal İlişkiler", "Aile",
    "Sağlık", "Finans ve Para", "Teknoloji", "Kişisel Gelişim", "Genel Günlük"
]
ENTITY_TYPES = ['PER', 'ORG', 'LOC']

def connect_supabase():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print(f"❌ HATA: {e}")
        return None

def fetch_data_from_supabase(supabase: Client):
    try:
        data, count = supabase.table('gunluk_girisler').select('created_at, analiz_sonucu').range(0, 5000).execute()
        print(f"✓ Veritabanından {len(data[1])} adet kayıt çekildi.")
        return data[1]
    except Exception as e:
        print(f"❌ HATA: {e}")
        return []

def process_data(raw_data):
    print("\n📊 Veri işleme başlıyor...")
    df = pd.DataFrame(raw_data)
    if df.empty: return None
    
    if isinstance(df['analiz_sonucu'].iloc[0], str):
        df['analiz_sonucu'] = df['analiz_sonucu'].apply(json.loads)
    
    analiz_df = pd.json_normalize(df['analiz_sonucu'])
    analiz_df = analiz_df.rename(columns={
        'sentiment.duygu': 'duygu',
        'sentiment.skor': 'duygu_skoru',
        'metrics.kelime_sayisi': 'kelime_sayisi',
        'metrics.karakter_sayisi': 'karakter_sayisi'
    })
    
    df = pd.concat([df.drop(columns=['analiz_sonucu']), analiz_df], axis=1)
    
    # --- TARİH ÖZELLİKLERİ ---
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['gun'] = df['created_at'].dt.dayofweek
    df['saat'] = df['created_at'].dt.hour
    df['hafta_sonu'] = df['gun'].isin([5, 6]).astype(int)
    
    def get_time_period(hour):
        if 0 <= hour < 6: return 'gece'
        elif 6 <= hour < 12: return 'sabah'
        elif 12 <= hour < 18: return 'ogle'
        else: return 'aksam'
    
    df['zaman_dilimi'] = df['saat'].apply(get_time_period)
    df = pd.get_dummies(df, columns=['gun', 'zaman_dilimi'], prefix=['gun', 'zaman'])
    
    # --- DUYGU SKORU DÜZELTMESİ (İŞARETLİ SKOR) ---
    # Negatifse -1 ile çarp
    df.loc[df['duygu'] == 'negative', 'duygu_skoru'] = df['duygu_skoru'] * -1
    df.loc[df['duygu'] == 'neutral', 'duygu_skoru'] = 0
    
    duygu_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    df['duygu_label'] = df['duygu'].map(duygu_map)
    
    # --- KONULAR ---
    df['topics'] = df['topics'].apply(lambda x: x if isinstance(x, list) else [])
    for konu in KONU_LISTESI:
        konu_key = konu.replace(' ', '_').replace('İ', 'I').lower()
        df[f'konu_{konu_key}'] = df['topics'].apply(lambda x: 1 if konu in x else 0)
    
    # --- VARLIKLAR ---
    df['entities'] = df['entities'].apply(lambda x: x if isinstance(x, list) else [])
    df['varlik_toplam_sayi'] = df['entities'].apply(len)
    
    def count_entity_types(entities_list):
        types = [entity.get('varlik', '') for entity in entities_list]
        return Counter(types)
    
    entity_counts = df['entities'].apply(count_entity_types).apply(pd.Series).fillna(0)
    for entity_type in ENTITY_TYPES:
        col_name = f'varlik_sayisi_{entity_type}'
        if entity_type in entity_counts.columns:
            df[col_name] = entity_counts[entity_type]
        else:
            df[col_name] = 0
            
    df = df.drop(columns=['created_at', 'duygu', 'topics', 'entities'])
    df = df.fillna(0)

    # --- 🔥 ZEKİ MOD PUANI SİMÜLASYONU ---
    print("🎲 Zeki Mod Puanı simüle ediliyor (Konu + Duygu)...")
    
    def simulate_smart_mood(row):
        score = row['duygu_skoru'] # -1 ile 1 arası
        
        # 1. Baz Puan (Duyguya göre)
        # -1 -> 1.5, 0 -> 3.0, 1 -> 4.5 (Ortalama)
        mood = 3.0 + (score * 1.5)
        
        # 2. Konu Etkisi (Bonuslar/Cezalar)
        # Bu kısım, modelin "Konu" öğrenmesini sağlayacak!
        if row['konu_sosyal_ilişkiler'] == 1: mood += 0.4  # Arkadaşlar iyi hissettirir
        if row['konu_kişisel_gelişim'] == 1: mood += 0.3   # Başarı hissi
        if row['konu_sağlık'] == 1 and score < 0: mood -= 0.5 # Hasta olmak ekstra kötü hissettirir
        if row['konu_finans_ve_para'] == 1 and score < 0: mood -= 0.3 # Para kaybı üzer
        if row['hafta_sonu'] == 1 and score > 0: mood += 0.2 # Hafta sonu mutluluğu
        
        # 3. Doğal Gürültü
        noise = np.random.normal(0, 0.3)
        mood += noise
        
        return max(1, min(5, int(round(mood))))

    # axis=1 diyerek her satır için ayrı hesapla
    df['user_mood'] = df.apply(simulate_smart_mood, axis=1)
    # ---------------------------------------------------------------

    # Scaling
    continuous_cols = ['kelime_sayisi', 'karakter_sayisi', 'duygu_skoru', 'varlik_toplam_sayi']
    scaler = StandardScaler()
    df[continuous_cols] = scaler.fit_transform(df[continuous_cols])
    
    with open('scaler.pkl', 'wb') as f: pickle.dump(scaler, f)
    
    return df

def split_and_save(df):
    print("\n✂️ Veri setleri oluşturuluyor...")
    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, shuffle=True)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    
    train_df.to_csv('train_data.csv', index=False)
    val_df.to_csv('val_data.csv', index=False)
    test_df.to_csv('test_data.csv', index=False)
    print(f"✓ Dosyalar kaydedildi.")

if __name__ == "__main__":
    print("🚀 MODEL VERİ HAZIRLAMA (ZEKİ SİMÜLASYON)")
    supabase = connect_supabase()
    if supabase:
        raw = fetch_data_from_supabase(supabase)
        if len(raw) >= MIN_REQUIRED_SAMPLES:
            df = process_data(raw)
            if df is not None: split_and_save(df)