# nlp_pipeline.py 

from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import logging

logging.basicConfig(level=logging.INFO)
print("NLP Pipeline modülü yükleniyor...")

try:
    
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="savasy/bert-base-turkish-sentiment-cased"
    )
    print("✓ Duygu analizi modeli yüklendi.")

    
    ner_pipeline = pipeline(
        "ner",
        model="savasy/bert-base-turkish-ner-cased",
        tokenizer="savasy/bert-base-turkish-ner-cased",
        aggregation_strategy="simple"
    )
    print("✓ NER modeli yüklendi.")

    
    sbert_model_name = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"
    sbert_tokenizer = AutoTokenizer.from_pretrained(sbert_model_name)
    sbert_model = AutoModel.from_pretrained(sbert_model_name)
    
    def mean_pooling(model_output, attention_mask):
        """Token embedding'lerinin ortalamasını alır"""
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def get_sentence_embedding(text):
        """Metin için embedding vektörü üretir"""
        encoded_input = sbert_tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
        with torch.no_grad():
            model_output = sbert_model(**encoded_input)
        return mean_pooling(model_output, encoded_input['attention_mask'])
    
    
    KONU_ETIKETLERI = {
        "İş ve Kariyer": "iş toplantı patron müdür proje görev şirket ofis maaş terfi kariyer işyeri mesai",
        "Eğitim ve Okul": "okul ders öğretmen sınav ödev üniversite öğrenci not eğitim",
        "Sosyal İlişkiler": "arkadaş buluşma dostluk sosyal ilişki dost sohbet eğlence",
        "Aile": "anne baba kardeş aile çocuk ebeveyn akraba ev yuva",
        "Sağlık": "hastane doktor sağlık hastalık ilaç tedavi eczane vitamin hasta tahlil muayene kilo diyet spor halsiz rahatsız ağrı acı yorgun grip nezle",
        "Finans ve Para": "para maaş banka kredi alışveriş borç tasarruf yatırım harcama ödeme market",
        "Teknoloji": "bilgisayar telefon internet uygulama yazılım teknoloji dijital online oyun",
        "Kişisel Gelişim": "hedef motivasyon öğrenme kitap okuma özgüven başarı kariyer planı eğitim semineri",
        "Genel Günlük": "bugün gün günlük rutin normal gündelik sabah akşam"
    }
    
    
    HARD_KEYWORDS = {
        "İş ve Kariyer": ["iş", "işe", "işten", "işyeri", "patron", "patronum", "müdür", "toplantı", "proje", "görev", "ofis", "mesai", "şirket"],
        "Eğitim ve Okul": ["okul", "okula", "okulda", "okuldan", "ders", "derste", "öğretmen", "sınav", "ödev", "üniversite", "öğrenci"],
        "Aile": ["anne", "annem", "annemi", "baba", "babam", "babamı", "babamla", "kardeş", "kardeşim", "aile", "çocuk", "çocuğum", "ebeveyn"],
        "Sağlık": ["hastane", "hastaneye", "hastanede", "hastaneden", "doktor", "doktora", "hasta", "hastalık", "ilaç", "tedavi", "eczane", "vitamin", "tahlil", "ağrı", "acı", "grip", "spor", "spora", "sporu"],
        "Finans ve Para": ["para", "parası", "maaş", "banka", "kredi", "borç", "ödeme", "alışveriş", "alışverişe", "market", "satın", "harcama", "ücret"],
        "Teknoloji": ["bilgisayar", "telefon", "internet", "uygulama", "yazılım", "oyun", "online"],
        "Kişisel Gelişim": ["hedef", "motivasyon", "başarı", "gelişim", "kitap", "kitabı", "oku", "okuma", "okuyorum"],
    }
    
    
    CONTEXTUAL_KEYWORDS = {
        "Finans ve Para": ["aldım", "aldı"],  
    }
    
    
    konu_embeddings = {}
    for konu, keywords in KONU_ETIKETLERI.items():
        konu_embeddings[konu] = F.normalize(get_sentence_embedding(keywords), p=2, dim=1)
    
    def classify_topics(text, primary_threshold=0.22, secondary_threshold=0.18):
        """
        HİBRİT YAKLAŞIM: Cosine similarity + Hard keyword matching + Contextual filtering
        """
        text_lower = text.lower()
        text_embedding = F.normalize(get_sentence_embedding(text), p=2, dim=1)
        
        results = []
        for konu, konu_emb in konu_embeddings.items():
            similarity = F.cosine_similarity(text_embedding, konu_emb).item()
            
            # HARD KEYWORD BOOST
            keyword_boost = 0.0
            matched_keywords = []
            if konu in HARD_KEYWORDS:
                for keyword in HARD_KEYWORDS[konu]:
                    # SUBSTRING KONTROLÜ: Kelimenin başında/sonunda boşluk olmalı
                    # Örnek: "iş" kelimesi "alışveriş" içinde geçmesin
                    if f" {keyword} " in f" {text_lower} " or text_lower.startswith(keyword + " ") or text_lower.endswith(" " + keyword):
                        keyword_boost = 0.15
                        matched_keywords.append(keyword)
                        break
            
            # BAĞLAMSAL FİLTRE: Bazı keyword'ler yalnızca güçlü semantic skorla kabul edilir
            if konu in CONTEXTUAL_KEYWORDS and keyword_boost > 0:
                for ctx_keyword in CONTEXTUAL_KEYWORDS[konu]:
                    if ctx_keyword in matched_keywords:
                        # Eğer bu bağlamsal kelimeyse ve base skor düşükse, boost'u iptal et
                        if similarity < 0.18:  # Threshold yükseltildi (0.15 → 0.18)
                            keyword_boost = 0.0
                            matched_keywords = []
                            break
            
            final_score = similarity + keyword_boost
            results.append((konu, final_score, similarity, keyword_boost, matched_keywords))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        # DEBUG
        print(f"\n🔍 KONU SKORLARI ('{text[:50]}...'):")
        for konu, final, orig, boost, keywords in results[:6]:
            boost_str = f" (+{boost:.2f} boost)" if boost > 0 else ""
            keyword_str = f" [matched: {keywords[0]}]" if keywords else ""
            print(f"  {konu}: {final:.4f} (base: {orig:.4f}{boost_str}{keyword_str})")
        
        topics = []
        
        # STRATEJİ 1: Primary threshold
        for konu, final_score, _, _, _ in results:
            if final_score >= primary_threshold and konu != "Genel Günlük":
                topics.append(konu)
                print(f"  ✅ Konu eklendi: {konu} ({final_score:.4f})")
        
        # STRATEJİ 2: Secondary threshold
        if not topics:
            for konu, final_score, _, _, _ in results:
                if final_score >= secondary_threshold and konu != "Genel Günlük":
                    topics.append(konu)
                    print(f"  ➕ İkincil konu: {konu} ({final_score:.4f})")
        
        # STRATEJİ 3: Fallback
        if not topics:
            best_topic, best_score, _, _, _ = results[0]
            if best_score > 0.12:
                topics.append(best_topic)
                print(f"  ⚠️ Fallback: {best_topic} ({best_score:.4f})")
        
        # Maksimum 3 konu
        topics = topics[:3]
        
        return topics
    
    zero_shot_pipeline = classify_topics
    print("✓ Sentence-BERT (Konu Sınıflandırma) yüklendi.")

except Exception as e:
    print(f"HATA: Modeller yüklenirken bir sorun oluştu: {e}")
    sentiment_pipeline = None
    ner_pipeline = None
    zero_shot_pipeline = None


# --- AYARLAR ---
NER_THRESHOLD = 0.70
SENTIMENT_THRESHOLD = 0.75
MIN_WORD_COUNT = 3


def analyze_text(text: str) -> dict:
    """Gelen metni duygu, NER ve konu analiziyle işler"""
    if not sentiment_pipeline or not ner_pipeline or not zero_shot_pipeline:
        print("HATA: NLP modelleri yüklenemedi, analiz yapılamıyor.")
        return {"hata": "NLP modelleri yüklenemedi."}

    # --- KORUMA KALKANI ---
    stripped_text = text.strip()
    word_count = len(stripped_text.split())
    char_count = len(stripped_text)
    
    metrics = {
        "kelime_sayisi": word_count,
        "karakter_sayisi": char_count
    }

    is_question = stripped_text.endswith('?')
    is_too_short = word_count < MIN_WORD_COUNT 

    if is_question or is_too_short:
        print(f"Kısa/Soru cümlesi algılandı. NLP analizi atlanıyor.")
        return {
            "sentiment": {"duygu": "neutral", "skor": 1.0},
            "entities": [],
            "topics": [],
            "metrics": metrics
        }
    
    # --- ANALİZ ---
    try:
        # 1. DUYGU ANALİZİ
        sentiment_result = sentiment_pipeline(stripped_text)[0]
        original_label = sentiment_result["label"]
        original_score = float(round(sentiment_result["score"], 4))
        
        final_label = "neutral" if original_score < SENTIMENT_THRESHOLD else original_label
        sentiment = {"duygu": final_label, "skor": original_score}

        # 2. VARLIK TANIMA
        ner_result = ner_pipeline(stripped_text)
        entities = [
            {
                "varlik": entity["entity_group"],
                "metin": entity["word"],
                "skor": float(round(entity["score"], 4))
            } for entity in ner_result if entity["score"] > NER_THRESHOLD
        ]
        
        # 3. KONU SINIFLANDIRMA (Sentence-BERT)
        topics = zero_shot_pipeline(stripped_text)
        
        return {
            "sentiment": sentiment,
            "entities": entities,
            "topics": topics,
            "metrics": metrics
        }

    except Exception as e:
        print(f"Analiz sırasında hata: {e}")
        import traceback
        traceback.print_exc()
        return {"hata": f"Metin analizi sırasında hata: {str(e)}"}


# TEST BLOĞU
if __name__ == "__main__":
    print("\n--- NLP Pipeline Test ---")
    
    if not sentiment_pipeline or not ner_pipeline or not zero_shot_pipeline:
        print("❌ Modeller yüklenemedi.")
    else:
        import json
        
        tests = [
            "Bugün hastaneye gidip kan değerlerimi incelettirdim. Doktor vitamin almam gerektiğini söyledi.",
            "Patronumla başarılı bir toplantı geçirdik.",
            "Okuldaki sınavım çok iyiydi, arkadaşlarımla kutladık.",
            "Annem hastalandı, hastaneye gittik."
        ]
        
        for test in tests:
            print(f"\n📝 Metin: {test}")
            result = analyze_text(test)
            print(json.dumps(result, indent=2, ensure_ascii=False))