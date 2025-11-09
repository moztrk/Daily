# prepare_data.py (İYİLEŞTİRİLMİŞ VERSIYON)

import os
import pandas as pd
import json
import pickle
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Konfigürasyon
MIN_REQUIRED_SAMPLES = 200  # Model için minimum örnek sayısı
KONU_LISTESI = [
    "İş ve Kariyer", "Eğitim ve Okul", "Sosyal İlişkiler", "Aile",
    "Sağlık", "Finans ve Para", "Teknoloji", "Kişisel Gelişim", "Genel Günlük"
]
ENTITY_TYPES = ['PER', 'ORG', 'LOC']

def connect_supabase():
    """Supabase'e bağlanır ve client'ı döndürür."""
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    try:
        supabase: Client = create_client(url, key)
        print("✓ Supabase bağlantısı başarılı.")
        return supabase
    except Exception as e:
        print(f"❌ HATA: Supabase bağlantısı kurulamadı: {e}")
        return None

def fetch_data_from_supabase(supabase: Client):
    """Veritabanından tüm 'gunluk_girisler' verisini çeker."""
    try:
        data, count = supabase.table('gunluk_girisler').select('created_at, analiz_sonucu').execute()
        print(f"✓ Veritabanından {len(data[1])} adet kayıt çekildi.")
        return data[1]
    except Exception as e:
        print(f"❌ HATA: Veri çekilemedi: {e}")
        return []

def process_data(raw_data):
    """Ham veriyi işler ve model için hazırlar."""
    print("\n📊 Veri işleme başlıyor...")
    
    # 1. DataFrame oluştur
    df = pd.DataFrame(raw_data)
    if df.empty:
        print("❌ İşlenecek veri yok.")
        return None
    
    # 2. JSON string'leri parse et
    if isinstance(df['analiz_sonucu'].iloc[0], str):
        df['analiz_sonucu'] = df['analiz_sonucu'].apply(json.loads)
    
    # 3. JSON'ı flatten et
    analiz_df = pd.json_normalize(df['analiz_sonucu'])
    analiz_df = analiz_df.rename(columns={
        'sentiment.duygu': 'duygu',
        'sentiment.skor': 'duygu_skoru',
        'metrics.kelime_sayisi': 'kelime_sayisi',
        'metrics.karakter_sayisi': 'karakter_sayisi'
    })
    
    df = pd.concat([df.drop(columns=['analiz_sonucu']), analiz_df], axis=1)
    
    # --- ÖZELLİK MÜHENDİSLİĞİ ---
    
    # 4. Tarih özellikleri
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['gun'] = df['created_at'].dt.dayofweek
    df['saat'] = df['created_at'].dt.hour
    df['ay'] = df['created_at'].dt.month
    df['hafta'] = df['created_at'].dt.isocalendar().week
    df['hafta_sonu'] = df['gun'].isin([5, 6]).astype(int)
    
    # Gün içi zaman dilimi
    def get_time_period(hour):
        if 0 <= hour < 6:
            return 'gece'
        elif 6 <= hour < 12:
            return 'sabah'
        elif 12 <= hour < 18:
            return 'ogle'
        else:
            return 'aksam'
    
    df['zaman_dilimi'] = df['saat'].apply(get_time_period)
    
    # One-hot encoding
    df = pd.get_dummies(df, columns=['gun', 'zaman_dilimi'], prefix=['gun', 'zaman'])
    
    # 5. Duygu label encoding
    duygu_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    df['duygu_label'] = df['duygu'].map(duygu_map)
    
    # 6. Topics multi-label binarization
    df['topics'] = df['topics'].apply(
        lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [])
    )
    
    for konu in KONU_LISTESI:
        konu_key = konu.replace(' ', '_').replace('İ', 'I').lower()
        df[f'konu_{konu_key}'] = df['topics'].apply(lambda x: 1 if konu in x else 0)
    
    # 7. Entities features
    df['entities'] = df['entities'].apply(
        lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [])
    )
    df['varlik_toplam_sayi'] = df['entities'].apply(len)
    
    def count_entity_types(entities_list):
        types = [entity.get('varlik', '') for entity in entities_list]
        return Counter(types)
    
    entity_counts = df['entities'].apply(count_entity_types).apply(pd.Series).fillna(0)
    
    # Tüm entity tiplerinin sütunlarını oluştur
    for entity_type in ENTITY_TYPES:
        col_name = f'varlik_sayisi_{entity_type}'
        if entity_type in entity_counts.columns:
            df[col_name] = entity_counts[entity_type]
        else:
            df[col_name] = 0
    
    # 8. Gereksiz sütunları kaldır
    df = df.drop(columns=['created_at', 'duygu', 'topics', 'entities'])
    
    # 9. NaN değerleri doldur
    df = df.fillna(0)
    
    # 10. Feature scaling
    continuous_cols = ['kelime_sayisi', 'karakter_sayisi', 'duygu_skoru', 'varlik_toplam_sayi']
    scaler = StandardScaler()
    df[continuous_cols] = scaler.fit_transform(df[continuous_cols])
    
    # Scaler'ı kaydet
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("✓ Feature scaler kaydedildi: scaler.pkl")
    
    print(f"✓ Veri işleme tamamlandı. Final boyut: {df.shape}")
    
    return df

def validate_data(df):
    """Veri kalitesi kontrolü"""
    print("\n🔍 Veri kalitesi kontrolleri yapılıyor...")
    issues = []
    
    # 1. Null check
    null_counts = df.isnull().sum()
    if null_counts.any():
        issues.append(f"⚠️ Null değerler var: {null_counts[null_counts > 0].to_dict()}")
    
    # 2. Duygu skoru aralığı
    if 'duygu_skoru' in df.columns:
        invalid_scores = ((df['duygu_skoru'] < -3) | (df['duygu_skoru'] > 3)).sum()
        if invalid_scores > 0:
            issues.append(f"⚠️ {invalid_scores} adet anormal duygu skoru!")
    
    # 3. Kelime sayısı
    if 'kelime_sayisi' in df.columns:
        too_short = (df['kelime_sayisi'] < -2).sum()  # Scaled değer
        if too_short > 0:
            issues.append(f"⚠️ {too_short} adet çok kısa entry!")
    
    # 4. Topic dağılımı
    topic_cols = [col for col in df.columns if col.startswith('konu_')]
    if topic_cols:
        topic_dist = df[topic_cols].sum().sort_values(ascending=False)
        print(f"\n📊 Konu Dağılımı:\n{topic_dist}")
    
    # 5. Sentiment dağılımı
    if 'duygu_label' in df.columns:
        sentiment_dist = df['duygu_label'].value_counts()
        print(f"\n😊 Duygu Dağılımı:\n{sentiment_dist}")
    
    if issues:
        print("\n⚠️ Veri kalitesi uyarıları:")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ Veri kalitesi kontrolleri başarılı!")
    
    return len(issues) == 0

def split_and_save(df):
    """Veriyi train/val/test olarak böl ve kaydet"""
    print("\n✂️ Veri setleri oluşturuluyor...")
    
    # %70 train, %15 validation, %15 test
    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, shuffle=True)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    
    # Kaydet
    train_df.to_csv('train_data.csv', index=False)
    val_df.to_csv('val_data.csv', index=False)
    test_df.to_csv('test_data.csv', index=False)
    
    print(f"✓ Train: {len(train_df)} örnek → train_data.csv")
    print(f"✓ Validation: {len(val_df)} örnek → val_data.csv")
    print(f"✓ Test: {len(test_df)} örnek → test_data.csv")
    
    # Özet istatistikler
    print(f"\n📈 Toplam veri: {len(df)} örnek")
    print(f"   - Train: %{len(train_df)/len(df)*100:.1f}")
    print(f"   - Val: %{len(val_df)/len(df)*100:.1f}")
    print(f"   - Test: %{len(test_df)/len(df)*100:.1f}")

# --- ANA ÇALIŞTIRMA ---
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MODEL VERİ HAZIRLAMA PIPELINE'I")
    print("=" * 60)
    
    supabase_client = connect_supabase()
    
    if not supabase_client:
        print("❌ Supabase bağlantısı kurulamadı. Çıkılıyor...")
        exit(1)
    
    # Veriyi çek
    raw_data = fetch_data_from_supabase(supabase_client)
    
    # Minimum veri kontrolü
    if len(raw_data) < MIN_REQUIRED_SAMPLES:
        print(f"\n⚠️ UYARI: Sadece {len(raw_data)} entry var!")
        print(f"❌ Model eğitimi için minimum {MIN_REQUIRED_SAMPLES} örnek gerekli.")
        print("\n💡 Öneriler:")
        print("   1. Daha fazla günlük yazısı yazılmasını bekle")
        print("   2. Mevcut veriyle basit istatistiksel analiz yap")
        print("   3. Pre-trained Türkçe sentiment model kullan (transfer learning)")
        exit(1)
    
    # Veriyi işle
    model_ready_df = process_data(raw_data)
    
    if model_ready_df is None:
        print("❌ Veri işleme başarısız. Çıkılıyor...")
        exit(1)
    
    # Veri kalitesi kontrolü
    if not validate_data(model_ready_df):
        print("\n⚠️ Veri kalitesi sorunları tespit edildi!")
        response = input("Devam etmek istiyor musunuz? (y/n): ")
        if response.lower() != 'y':
            exit(1)
    
    # Train/val/test split
    split_and_save(model_ready_df)
    
    print("\n" + "=" * 60)
    print("✅ VERİ HAZIRLAMA TAMAMLANDI!")
    print("=" * 60)
    print("\n📁 Oluşturulan dosyalar:")
    print("   - train_data.csv")
    print("   - val_data.csv")
    print("   - test_data.csv")
    print("   - scaler.pkl")
    print("\n🎯 Sonraki adım: Model eğitimi (train_model.py)")