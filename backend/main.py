import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client

# .env dosyasındaki bilgileri yükle
load_dotenv()

# Supabase bilgilerini al
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# FastAPI uygulamasını oluştur
app = FastAPI()

# Mobil uygulamadan gelecek JSON'ın nasıl görüneceğini tanımla
class Girdi(BaseModel):
    metin: str

# Ana route ("/") için bir GET endpoint'i (bu test için kalabilir)
@app.get("/")
async def root():
    return {"mesaj": "Merhaba Dünya, sunucu çalışıyor!"}

# YENİ ENDPOINT: Günlük girdisini kaydetmek için
@app.post("/entries")
async def create_entry(girdi: Girdi):
    try:
        # Gelen veriyi 'gunluk_girisler' tablosuna ekle
        data, count = supabase.table('gunluk_girisler').insert({"metin": girdi.metin}).execute()
        
        # Başarılı olursa, eklenen verinin kendisini döndür
        return {"status": "success", "data": data[1][0]}
    except Exception as e:
        # Bir hata olursa, hatayı döndür
        return {"status": "error", "message": str(e)}