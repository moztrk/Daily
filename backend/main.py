# main.py 

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware  # CORS eklendi
from nlp_pipeline import analyze_text  # NLP modülümüz import edildi

# .env dosyasındaki bilgileri yükle
load_dotenv()

# Supabase bilgilerini al
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

try:
    supabase: Client = create_client(url, key)
except Exception as e:
    print(f"Supabase client oluşturulamadı: {e}")
    supabase = None

# FastAPI uygulamasını oluştur
app = FastAPI()

# YENİ EKLENDİ: CORS Middleware
# React Native uygulamasının bu API'ye erişebilmesi için bu gerekli.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prototipten sonra burayı kısıtla!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Girdi(BaseModel):
    metin: str

# Ana route ("/") için bir GET endpoint'i
@app.get("/")
async def root():
    return {"mesaj": "Merhaba Dünya, NLP sunucusu çalışıyor!"}

# GÜNCELLENMİS ENDPOINT: Günlük girdisini kaydetmek için
@app.post("/entries")
async def create_entry(girdi: Girdi):
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Veritabanı bağlantısı kurulamadı.")

    # 1. NLP ANALİZİNİ ÇALIŞTIR
    try:
        print(f"Metin analiz ediliyor: {girdi.metin}")
        analiz_sonucu = analyze_text(girdi.metin)
        print(f"Analiz sonucu: {analiz_sonucu}")
        
        # Eğer nlp_pipeline'da bir hata olduysa (örn: modeller yüklenemedi)
        if analiz_sonucu.get("hata"):
            raise HTTPException(status_code=500, detail=analiz_sonucu.get("hata"))
            
    except Exception as e:
        # NLP sırasında beklenmedik bir hata olursa
        raise HTTPException(status_code=500, detail=f"NLP analizi sırasında hata oluştu: {str(e)}")

    # 2. VERİTABANINA KAYDET
    try:
        # Gelen veriyi VE ANALİZ SONUCUNU 'gunluk_girisler' tablosuna ekle
        data, count = supabase.table('gunluk_girisler').insert({
            "metin": girdi.metin,
            "analiz_sonucu": analiz_sonucu  # <-- GÜNCELLENEN KISIM
        }).execute()
        
        # Başarılı olursa, eklenen verinin kendisini döndür
        return {"status": "success", "data": data[1][0]}
    
    except Exception as e:
        # Bir hata olursa, HTTP 500 hatası döndür (bu daha standart bir yöntem)
        raise HTTPException(status_code=500, detail=f"Veritabanına kayıt sırasında hata: {str(e)}")