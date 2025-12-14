🧠 DailyMind: Yapay Zeka Destekli Kişisel Analiz Motoru

DailyMind, kullanıcının günlük metin girdilerini modern Doğal Dil İşleme (NLP) teknikleri ile analiz eden ve Makine Öğrenmesi algoritmaları kullanarak kullanıcının ruh halini tahminleyen akıllı bir mobil uygulamadır.

Bu proje, sadece veri depolayan klasik günlük uygulamalarından farklı olarak, veriden anlam çıkaran ve kullanıcıya kişiselleştirilmiş içgörüler sunan bir karar destek sistemi olarak tasarlanmıştır.

🚀 Temel Özellikler

📝 Akıllı Günlük Tutma: Kullanıcı dostu mobil arayüz üzerinden günlük girişi.

🤖 NLP Analiz Pipeline'ı: Her metin girdisi anlık olarak işlenir:

Duygu Analizi: Metnin pozitif, negatif veya nötr durumu ve güven skoru (BERT).

Varlık İsmi Tanıma (NER): Metindeki kişi, kurum ve yer isimlerinin tespiti.

Konu Sınıflandırma: Sentence-BERT ve Kosinüs Benzerliği kullanan hibrit bir algoritma ile metnin konusunun (İş, Sağlık, Aile vb.) belirlenmesi.

🔮 Mod Tahminleme: Eğitilmiş Random Forest Regressor modeli, metin özelliklerine bakarak kullanıcının o günkü modunu (1-5 arası) tahmin eder.

💡 Kişiselleştirilmiş İçgörüler: Sistem, geçmiş verilere bakarak "İş konuları modunu düşürüyor" gibi otomatik tavsiyeler üretir.

📊 Görsel Raporlama: Duygu trendleri ve konu dağılımlarını gösteren interaktif grafikler.

🛠️ Teknolojik Altyapı

Backend ve Yapay Zeka

API Framework: Python FastAPI

NLP Modelleri:

Duygu & NER: savasy/bert-base-turkish modelleri.

Konu Modelleme: emrecan/bert-base-turkish-cased-mean-nli-stsb-tr (SBERT).

Makine Öğrenmesi: Scikit-learn (Random Forest, StandardScaler).

Veri Seti: Proje kapsamında oluşturulan 3.000+ satırlık yapılandırılmış veri seti ile model eğitimi gerçekleştirilmiştir.

Frontend (Mobil)

Framework: React Native (Expo)

Navigasyon: React Navigation

Görselleştirme: react-native-chart-kit

Veritabanı

Platform: Supabase (PostgreSQL)

📂 Proje Mimarisi

```
Daily/
├── backend/
│   ├── main.py                 # API ve Yapay Zeka Entegrasyon Noktası
│   ├── nlp_pipeline.py         # NLP Motoru (BERT, SBERT Algoritmaları)
│   ├── train_regressor.py      # Makine Öğrenmesi Eğitim Betiği
│   ├── prepare_data.py         # Veri Ön İşleme ve Özellik Mühendisliği
│   └── mood_regressor.pkl      # Eğitilmiş Model Dosyası
│
└── mobil/mobile-app/
    ├── screens/                # Arayüz Ekranları (Ana Sayfa, Raporlar...)
    ├── navigation/             # Uygulama İçi Yönlendirme
    └── services/               # Backend ile Haberleşme Servisi
```

⚙️ Kurulum ve Çalıştırma

1. Backend Kurulumu

```bash
cd backend
pip install -r requirements.txt
```

.env dosyasını oluşturun ve Supabase anahtarlarını girin.

Sunucuyu Başlatma:

```bash
uvicorn main:app --reload --host 0.0.0.0
```

2. Mobil Uygulama Kurulumu

```bash
cd mobil/mobile-app
npm install
npx expo start
```

🧠 Algoritmik Yaklaşım

Sistem, metin verisini anlamlandırmak için çok katmanlı bir yaklaşım kullanır:

Vektörleştirme (Embedding): Metinler, Türkçe için eğitilmiş SBERT modeli ile 768 boyutlu vektör uzayına taşınır.

Hibrit Konu Tespiti: Vektör benzerliği (Cosine Similarity) ve Anahtar Kelime Desteği (Keyword Boosting) birleştirilerek en doğru konu etiketi bulunur.

Regresyon Analizi: Duygu skoru, konu etiketleri, zaman bilgisi ve varlık sayıları birleştirilerek 30+ özellikli bir matris oluşturulur ve Random Forest algoritması ile mod tahmini yapılır.

Performans: Model, test veri setinde yüksek doğruluk oranıyla tahmin yapmaktadır.

---

🧠 DailyMind: AI-Powered Personal Analysis Engine (English)

DailyMind is a mobile journaling application that goes beyond simple text storage. It utilizes advanced Natural Language Processing (NLP) and Machine Learning (ML) techniques to analyze user entries, extract hidden patterns, and predict mood fluctuations based on topics and entities.

🚀 Key Features

📝 Smart Journaling: Users can write daily entries via a clean mobile interface.

🤖 Advanced NLP Pipeline: Every entry is processed to extract:

Sentiment Analysis: (Positive, Negative, Neutral) with confidence scores.

Named Entity Recognition (NER): Detects people, organizations, and locations.

Topic Modeling: Automatically categorizes entries (e.g., Work, Health, Social) using a hybrid SBERT approach.

🔮 Mood Prediction Engine: A trained Random Forest Regressor predicts the user's mood score (1-5) based on the textual content, topics, and historical data.

💡 Personalized Insights: The system generates actionable insights (e.g., "Talking about 'Work' tends to lower your mood on Mondays").

📊 Visual Analytics: Interactive charts showing mood trends and topic distributions.

🛠️ Tech Stack

Backend & AI

Framework: Python FastAPI

NLP: Hugging Face Transformers (savasy/bert-base-turkish-sentiment-cased, savasy/bert-base-turkish-ner-cased)

Topic Modeling: Sentence-BERT (emrecan/bert-base-turkish-cased-mean-nli-stsb-tr) with Cosine Similarity & Keyword Boosting.

Machine Learning: Scikit-learn (Random Forest Regressor), Pandas, NumPy.

Dataset: Trained on a synthetic dataset of 3,000+ annotated journal entries.

Frontend (Mobile)

Framework: React Native (Expo)

Navigation: React Navigation (Stack & Bottom Tabs)

UI Components: Linear Gradients, Safe Area Context, Vector Icons.

Charts: react-native-chart-kit

Infrastructure

Database: Supabase (PostgreSQL)

📂 Project Structure

```
Daily/
├── backend/
│   ├── main.py                 # FastAPI Entry Point & API Endpoints
│   ├── nlp_pipeline.py         # NLP Logic (BERT, SBERT, NER)
│   ├── train_regressor.py      # ML Model Training Script
│   ├── prepare_data.py         # Data Preprocessing & Feature Engineering
│   ├── mood_regressor.pkl      # Trained ML Model
│   └── scaler.pkl              # Feature Scaler
│
└── mobil/mobile-app/
    ├── App.js                  # Mobile Entry Point
    ├── screens/                # UI Screens (Home, Reports, AddEntry...)
    ├── navigation/             # Routing Logic
    └── services/               # API Communication (ApiService.js)
```

⚙️ Installation & Setup

1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a .env file with your SUPABASE_URL and SUPABASE_KEY.

Run the Server:

```bash
uvicorn main:app --reload --host 0.0.0.0
```

2. Mobile App Setup

```bash
cd mobil/mobile-app
npm install
npx expo start
```

🧠 AI Architecture

The system uses a multi-stage pipeline to process data:

Text Ingestion: User inputs text.

NLP Analysis:

Sentiment: Determined via BERT. Scores are signed (Negative < 0, Positive > 0).

Topic Classification: Calculated using Semantic Similarity (Cosine) between the input embedding and pre-computed topic embeddings.

Feature Vectorization: The analysis is converted into a structured feature vector (One-hot encoded topics, entity counts, time of day).

Regression: The vector is passed to mood_regressor.pkl, which predicts the Mood Score.

Insight Generation: Rule-based logic correlates high/low scores with specific topics to generate advice.

📊 Dataset Status

The current model is trained on a dataset of approximately 3,000 entries, covering diverse topics such as Career, Health, Finance, and Social Relationships. The dataset includes simulated user mood scores to train the regression model effectively.