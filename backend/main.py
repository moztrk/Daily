from fastapi import FastAPI

# FastAPI uygulamasını oluştur
app = FastAPI()

# Ana route ("/") için bir GET endpoint'i tanımla
@app.get("/")
async def root():
    return {"mesaj": "Merhaba Dünya"}