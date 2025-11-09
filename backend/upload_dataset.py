# upload_dataset.py - Günlük örneklerini veritabanına yükle

import os
import sys
import time
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# nlp_pipeline'ı import et
sys.path.append(os.path.dirname(__file__))
from nlp_pipeline import analyze_text
from gunluk_dataset import GUNLUK_ORNEKLERI

def connect_supabase():
    """Supabase'e bağlan"""
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ HATA: .env dosyasında SUPABASE_URL ve SUPABASE_KEY bulunamadı!")
        return None
    
    try:
        supabase = create_client(url, key)
        print("✅ Supabase bağlantısı başarılı!")
        return supabase
    except Exception as e:
        print(f"❌ HATA: Supabase bağlantı hatası: {e}")
        return None

def generate_realistic_timestamp(index, total):
    """Gerçekçi tarih üret (son 60 gün içinde rastgele)"""
    # Son 60 günü kapsasın
    days_ago = random.randint(0, 60)
    
    # Günün saati (7-23 arası, insanlar genelde bu saatlerde yazar)
    hour = random.randint(7, 23)
    minute = random.randint(0, 59)
    
    timestamp = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=minute)
    return timestamp.isoformat()

def upload_entries(supabase: Client, entries: list, batch_size: int = 10):
    """Günlük girdilerini veritabanına yükle"""
    total = len(entries)
    success_count = 0
    failed_count = 0
    
    print(f"\n🚀 {total} adet günlük yükleniyor...")
    print("=" * 60)
    
    for i, entry_text in enumerate(entries, 1):
        try:
            # 1. Metni analiz et
            print(f"\n[{i}/{total}] Analiz ediliyor...")
            analysis = analyze_text(entry_text)
            
            if "hata" in analysis:
                print(f"   ⚠️ Analiz hatası, atlanıyor: {entry_text[:50]}...")
                failed_count += 1
                continue
            
            # 2. Gerçekçi tarih oluştur
            created_at = generate_realistic_timestamp(i, total)
            
            # 3. Veritabanına ekle
            data = {
                "metin": entry_text,
                "analiz_sonucu": analysis,
                "created_at": created_at
            }
            
            result = supabase.table('gunluk_girisler').insert(data).execute()
            
            if result.data:
                success_count += 1
                print(f"   ✅ Başarılı! ({success_count}/{total})")
                print(f"      Konu: {analysis.get('topics', [])}")
                print(f"      Duygu: {analysis['sentiment']['duygu']}")
            else:
                failed_count += 1
                print(f"   ❌ Veritabanı hatası!")
            
            # Rate limiting (Supabase API limitleri için)
            if i % batch_size == 0:
                print(f"\n   ⏳ {batch_size} entry yüklendi, 2 saniye bekleniyor...")
                time.sleep(2)
        
        except Exception as e:
            failed_count += 1
            print(f"   ❌ Hata: {e}")
            continue
    
    # Özet
    print("\n" + "=" * 60)
    print("📊 YÜKLEME ÖZETI")
    print("=" * 60)
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"📈 Toplam: {total}")
    print(f"🎯 Başarı Oranı: %{(success_count/total)*100:.1f}")
    print("=" * 60)

def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("🗄️ GÜNLÜK VERİ SETİ YÜKLEME ARACI")
    print("=" * 60)
    
    # Bağlantı kur
    supabase = connect_supabase()
    if not supabase:
        return
    
    # Onay al
    print(f"\n⚠️ UYARI: {len(GUNLUK_ORNEKLERI)} adet günlük veritabanına eklenecek!")
    print("Bu işlem 10-15 dakika sürebilir.")
    response = input("\nDevam etmek istiyor musunuz? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ İşlem iptal edildi.")
        return
    
    # Yükleme başlat
    upload_entries(supabase, GUNLUK_ORNEKLERI, batch_size=10)
    
    print("\n✅ Tüm işlemler tamamlandı!")
    print("📌 Sonraki adım: python prepare_data.py")

if __name__ == "__main__":
    main()