# nlp_pipeline.py (FİNAL SÜRÜM - Koruma Kalkanı v2 Eklendi)

from transformers import pipeline
import logging

# Hata ayıklama loglarını açalım
logging.basicConfig(level=logging.INFO)

print("NLP Pipeline modülü yükleniyor...")

try:
    # 1. DUYGU ANALİZİ PİPELINE'I
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="savasy/bert-base-turkish-sentiment-cased"
    )
    print("Duygu analizi modeli yüklendi.")

    # 2. ADLANDIRILMIŞ VARLIK TANIMA (NER) PİPELINE'I
    ner_pipeline = pipeline(
        "ner",
        model="savasy/bert-base-turkish-ner-cased",
        tokenizer="savasy/bert-base-turkish-ner-cased",
        aggregation_strategy="simple"
    )
    print("NER modeli yüklendi.")

    # 3. SIFIR-ATIMLI SINIFLANDIRMA (ZERO-SHOT CLASSIFICATION) PİPELINE'I
    zero_shot_pipeline = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
    print("Zero-shot (Konu Modelleme) yüklendi.")

except Exception as e:
    print(f"HATA: Modeller yüklenirken bir sorun oluştu: {e}")
    sentiment_pipeline = None
    ner_pipeline = None
    zero_shot_pipeline = None


# Sınıflandırma için kullanılacak konu etiketleri
KONU_ETIKETLERI = ["İş", "Okul", "Sosyal Hayat", "Aile", "Sağlık", "Finans", "Teknoloji", "Kişisel Gelişim"]

# --- GÜVEN EŞİKLERİ ---
NER_THRESHOLD = 0.70
TOPIC_THRESHOLD = 0.75
SENTIMENT_THRESHOLD = 0.75
# -------------------------
# --- KORUMA KALKANI AYARI ---
MIN_WORD_COUNT = 3  # <-- DÜZELTME BURADA (2'den 3'e çıktı)
# -------------------------


def analyze_text(text: str) -> dict:
    """
    Gelen metni duygu, NER ve konu analiziyle işler, ek metrikler hesaplar
    ve sonuçları tek bir dictionary olarak döndürür.
    """
    if not sentiment_pipeline or not ner_pipeline or not zero_shot_pipeline:
        print("HATA: NLP modelleri yüklenemedi, analiz yapılamıyor.")
        return {"hata": "NLP modelleri yüklenemedi."}

    # --- KORUMA KALKANI (GUARD CLAUSE) ---
    
    # 1. Metrikleri ve temel bilgileri hesapla
    stripped_text = text.strip()
    word_count = len(stripped_text.split())
    char_count = len(stripped_text)
    
    metrics = {
        "kelime_sayisi": word_count,
        "karakter_sayisi": char_count
    }

    # 2. Filtreleri uygula
    is_question = stripped_text.endswith('?')
    # GÜNCELLEME: Artık 3 kelimeden azsa (1 veya 2 kelime) "çok kısa" kabul edilecek
    is_too_short = word_count < MIN_WORD_COUNT 

    # 3. Eğer metin soruysa VEYA çok kısaysa, modelleri HİÇ ÇALIŞTIRMA.
    if is_question or is_too_short:
        print(f"Kısa/Soru cümlesi algılandı ('{text}'). NLP analizi atlanıyor.")
        
        # Direkt "Nötr" bir JSON döndür ve fonksiyondan çık.
        return {
            "sentiment": {"duygu": "neutral", "skor": 1.0}, # Nötr olarak etiketle
            "entities": [],
            "topics": [],
            "metrics": metrics # Metrikleri yine de gönder
        }
    
    # --- EĞER METİN BU KALKANI GEÇERSE, GERÇEK ANALİZ BAŞLAR ---
    
    try:
        # 1. DUYGU ANALİZİ - GÜVEN FİLTRELİ
        sentiment_result = sentiment_pipeline(stripped_text)[0]
        
        original_label = sentiment_result["label"]
        original_score = float(round(sentiment_result["score"], 4))
        
        if original_score < SENTIMENT_THRESHOLD:
            final_label = "neutral"
        else:
            final_label = original_label
            
        sentiment = {
            "duygu": final_label,
            "skor": original_score
        }

        # 2. VARLIK TANIMA (NER) - GÜVEN FİLTRELİ
        ner_result = ner_pipeline(stripped_text)
        
        entities = [
            {
                "varlik": entity["entity_group"],
                "metin": entity["word"],
                "skor": float(round(entity["score"], 4))
            } for entity in ner_result if entity["score"] > NER_THRESHOLD
        ]
        
        # 3. KONU MODELLEME - GÜVEN FİLTRELİ
        classification_result = zero_shot_pipeline(stripped_text, KONU_ETIKETLERI, multi_label=True)
        
        topics = [
            label for label, score in zip(classification_result['labels'], classification_result['scores']) 
            if score > TOPIC_THRESHOLD
        ]
        
        # 4. TÜM SONUÇLARI BİRLEŞTİR
        analysis_output = {
            "sentiment": sentiment,
            "entities": entities,
            "topics": topics,
            "metrics": metrics
        }
        
        return analysis_output

    except Exception as e:
        print(f"Analiz sırasında hata: {e}")
        return {"hata": "Metin analizi sırasında bir sorun oluştu."}

# Modülü test etmek için ana blok
if __name__ == "__main__":
    print("\n--- NLP Pipeline Test Başlatılıyor ---")
    
    if not sentiment_pipeline or not ner_pipeline or not zero_shot_pipeline:
        print("Modeller yüklenemediği için test çalıştırılamadı.")
    else:
        # 1. Test: Kalkanı test et (2 kelime)
        test_metni_1 = "Dün neredeydin"
        print(f"\nTest Metni 1: {test_metni_1}")
        sonuclar_1 = analyze_text(test_metni_1)
        import json
        print("Analiz Sonuçları 1:")
        print(json.dumps(sonuclar_1, indent=2, ensure_ascii=False))
        # Beklenti: neutral, entities: [], topics: [] (NLP analizi atlanıyor)

        # 2. Test: Kalkanı test et (soru işareti)
        test_metni_2 = "Yarın ne yapacaksın?"
        print(f"\nTest Metni 2: {test_metni_2}")
        sonuclar_2 = analyze_text(test_metni_2)
        print("Analiz Sonuçları 2:")
        print(json.dumps(sonuclar_2, indent=2, ensure_ascii=False))
        # Beklenti: neutral, entities: [], topics: [] (NLP analizi atlanıyor)

        # 3. Test: Kalkanı geçmesi gereken normal cümle (3 kelime)
        test_metni_3 = "Bugün çok mutluyum."
        print(f"\nTest Metni 3: {test_metni_3}")
        sonuclar_3 = analyze_text(test_metni_3)
        print("Analiz Sonuçları 3:")
        print(json.dumps(sonuclar_3, indent=2, ensure_ascii=False))
        # Beklenti: positive, entities: [], topics: [] (Analiz yapılacak)