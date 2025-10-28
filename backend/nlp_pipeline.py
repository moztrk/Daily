# nlp_pipeline.py (FİNAL - np.float32 DÜZELTMELİ SÜRÜM)

from transformers import pipeline
import logging

# Hata ayıklama loglarını açalım (model yüklenirken görmek için)
logging.basicConfig(level=logging.INFO)

print("NLP Pipeline modülü yükleniyor...")

try:
    # 1. DUYGU ANALİZİ PİPELINE'I (TÜRKÇE)
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="savasy/bert-base-turkish-sentiment-cased",
        tokenizer="savasy/bert-base-turkish-sentiment-cased"
    )
    print("Duygu analizi modeli yüklendi.")

    # 2. ADLANDIRILMIŞ VARLIK TANIMA (NER) PİPELINE'I (TÜRKÇE)
    ner_pipeline = pipeline(
        "ner",
        model="savasy/bert-base-turkish-ner-cased",
        tokenizer="savasy/bert-base-turkish-ner-cased",
        aggregation_strategy="simple"
    )
    print("NER modeli yüklendi.")

except Exception as e:
    print(f"HATA: Modeller yüklenirken bir sorun oluştu: {e}")
    sentiment_pipeline = None
    ner_pipeline = None

def analyze_text(text: str) -> dict:
    """
    Gelen metni hem duygu hem de NER analizinden geçirir
    ve sonuçları tek bir dictionary olarak döndürür.
    """
    if not sentiment_pipeline or not ner_pipeline:
        # main.py'nin bu hatayı yakalayabilmesi için
        print("HATA: NLP modelleri yüklenemedi, analiz yapılamıyor.")
        return {"hata": "NLP modelleri yüklenemedi."}

    try:
        # 1. Duygu analizini çalıştır
        sentiment_result = sentiment_pipeline(text)
        
        # 2. NER analizini çalıştır
        ner_result = ner_pipeline(text)

        # 3. Sonuçları birleştir
        # Düzgün bir JSON yapısı oluşturalım
        
        # NER sonucunu temizleyelim (sadece entity_group, word, score alalım)
        entities = [
            {
                "varlik": entity["entity_group"], # örn: PER, LOC, ORG
                "metin": entity["word"],
                # DÜZELTME: Gelen np.float32'yi standart float'a çevir
                "skor": float(round(entity["score"], 4))
            } for entity in ner_result
        ]

        # Duygu sonucunu temizleyelim (liste içinden ilk sonucu alalım)
        sentiment = {
            "duygu": sentiment_result[0]["label"], # örn: positive
            # DÜZELTME: Gelen np.float32'yi standart float'a çevir
            "skor": float(round(sentiment_result[0]["score"], 4))
        }

        analysis_output = {
            "sentiment": sentiment,
            "entities": entities
        }
        
        return analysis_output

    except Exception as e:
        print(f"Analiz sırasında hata: {e}")
        return {"hata": "Metin analizi sırasında bir sorun oluştu."}

# Modülün doğru çalışıp çalışmadığını test etmek için:
# Bu dosyayı doğrudan `python nlp_pipeline.py` ile çalıştırabilirsin.
if __name__ == "__main__":
    print("\n--- NLP Pipeline Test Başlatılıyor ---")
    
    # Modellerin yüklenip yüklenmediğini kontrol et
    if not sentiment_pipeline or not ner_pipeline:
        print("Modeller yüklenemediği için test çalıştırılamadı.")
    else:
        # np.float32 hatasını test eden bir cümle
        test_metni = "Ahmet Yılmaz, dün gece Google'ın İstanbul ofisinde bir toplantı yaptı. Mackbear'dan kahve aldı."
        
        print(f"Test Metni: {test_metni}")
        sonuclar = analyze_text(test_metni)
        
        import json
        print("\nAnaliz Sonuçları:")
        # Bu print'in patlamaması lazım
        print(json.dumps(sonuclar, indent=2, ensure_ascii=False))
        
        # Tipleri kontrol et
        if sonuclar.get("entities"):
            skor_tipi = type(sonuclar["entities"][0]["skor"])
            print(f"\nVarlık skor tipi: {skor_tipi}")
            if skor_tipi is float:
                print("Test BAŞARILI: Tip standart float.")
            else:
                print("Test BAŞARISIZ: Tip hala float değil.")