🧠 DailyMind: AI-Powered Personal Analysis Engine

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


⚙️ Installation & Setup

1. Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


Create a .env file with your SUPABASE_URL and SUPABASE_KEY.

Run the Server:

uvicorn main:app --reload --host 0.0.0.0


2. Mobile App Setup

cd mobil/mobile-app
npm install
npx expo start


🧠 AI Architecture

The system uses a multi-stage pipeline to process data:

Text Ingestion: User inputs text.

NLP Analysis: * Sentiment: Determined via BERT. Scores are signed (Negative < 0, Positive > 0).

Topic Classification: Calculated using Semantic Similarity (Cosine) between the input embedding and pre-computed topic embeddings.

Feature Vectorization: The analysis is converted into a structured feature vector (One-hot encoded topics, entity counts, time of day).

Regression: The vector is passed to mood_regressor.pkl, which predicts the Mood Score.

Insight Generation: Rule-based logic correlates high/low scores with specific topics to generate advice.

📊 Dataset Status

The current model is trained on a dataset of approximately 3,000 entries, covering diverse topics such as Career, Health, Finance, and Social Relationships. The dataset includes simulated user mood scores to train the regression model effectively.
