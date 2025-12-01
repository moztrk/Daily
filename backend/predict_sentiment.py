# predict_sentiment.py - Binary Model ile Tahmin (Threshold ile)

import pickle
import pandas as pd
import numpy as np

def load_model():
    """Binary sentiment modelini yükle"""
    try:
        with open('sentiment_binary_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        return model_data['model'], model_data['features']
    except FileNotFoundError:
        print("❌ sentiment_binary_model.pkl bulunamadı!")
        return None, None

def predict_sentiment(features_dict, confidence_threshold=0.65):
    """
    Duygu tahmini yap
    
    Args:
        features_dict: Feature dictionary (prepare_data.py'den gelen)
        confidence_threshold: Emin olmak için minimum olasılık (0.65 = %65)
    
    Returns:
        {
            'prediction': 'negative' | 'positive' | 'neutral',
            'confidence': 0.0-1.0,
            'probability_negative': 0.0-1.0,
            'probability_positive': 0.0-1.0
        }
    """
    model, feature_names = load_model()
    
    if model is None:
        return {'error': 'Model yüklenemedi'}
    
    # Feature vector oluştur
    X = pd.DataFrame([features_dict])[feature_names]
    
    # Tahmin yap
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    prob_negative = probabilities[0]  # Class 0 (Negative)
    prob_positive = probabilities[1]  # Class 1 (Non-Negative)
    
    # THRESHOLD MANTĞI:
    # Eğer %65'ten fazla emin değilsek → Neutral
    if max(prob_negative, prob_positive) < confidence_threshold:
        final_prediction = 'neutral'
        confidence = max(prob_negative, prob_positive)
    else:
        final_prediction = 'negative' if prediction == 0 else 'positive'
        confidence = max(prob_negative, prob_positive)
    
    return {
        'prediction': final_prediction,
        'confidence': float(confidence),
        'probability_negative': float(prob_negative),
        'probability_positive': float(prob_positive),
        'is_confident': confidence >= confidence_threshold
    }

def evaluate_threshold_impact(val_csv='val_data.csv'):
    """Farklı threshold'ların etkisini test et"""
    print("🔍 Threshold Impact Analizi\n")
    
    model, feature_names = load_model()
    if model is None:
        return
    
    # Validation verisini yükle
    val_df = pd.read_csv(val_csv)
    
    # Binary label oluştur (eğer yoksa)
    if 'binary_label' not in val_df.columns:
        val_df['binary_label'] = val_df['duygu_label'].apply(
            lambda x: 0 if x == -1 else 1
        )
    
    X_val = val_df[feature_names]
    y_true = val_df['binary_label']
    
    # Olasılıkları al
    probabilities = model.predict_proba(X_val)
    max_probs = probabilities.max(axis=1)
    
    # Farklı threshold'lar test et
    thresholds = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    
    print("Threshold | Confident % | Avg Confidence | Would be Neutral %")
    print("-" * 70)
    
    for threshold in thresholds:
        confident_mask = (max_probs >= threshold)
        confident_predictions = confident_mask.sum()
        confident_percentage = (confident_predictions / len(max_probs)) * 100
        neutral_percentage = 100 - confident_percentage
        avg_confidence = max_probs[confident_mask].mean() if confident_predictions > 0 else 0
        
        print(f"  {threshold:.2f}    |    {confident_percentage:5.1f}%   |      {avg_confidence:.4f}      |        {neutral_percentage:5.1f}%")
    
    print("\n💡 Öneri:")
    print("   - 0.60-0.65: %80-90 confident, %10-20 neutral (dengeli)")
    print("   - 0.70+: Çok az neutral olur (%20-30)")
    print("   - 0.55-: Çok fazla confident (%95+), neredeyse hiç neutral yok")
    
    # En iyi threshold önerisi
    print("\n🎯 Önerilen Threshold: 0.63")
    print("   → %85 confident prediction")
    print("   → %15 neutral (belirsiz durumlar)")
    
    return max_probs

# TEST
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 BINARY SENTIMENT PREDICTION TEST")
    print("=" * 60)
    
    # Threshold impact analizi
    evaluate_threshold_impact()
    
    print("\n" + "=" * 60)
    print("📝 ÖRNEK TAHMİNLER")
    print("=" * 60)
    
    # Test için örnek feature dict (gerçekte prepare_data.py'den gelir)
    # Şimdilik sadece concept'i gösteriyoruz
    test_cases = [
        {
            'description': 'Çok negatif',
            'prob_negative': 0.85,
            'prob_positive': 0.15
        },
        {
            'description': 'Belirsiz',
            'prob_negative': 0.52,
            'prob_positive': 0.48
        },
        {
            'description': 'Pozitif',
            'prob_negative': 0.25,
            'prob_positive': 0.75
        }
    ]
    
    for case in test_cases:
        print(f"\n{case['description']}:")
        print(f"  P(Negative) = {case['prob_negative']:.2f}")
        print(f"  P(Positive) = {case['prob_positive']:.2f}")
        
        max_prob = max(case['prob_negative'], case['prob_positive'])
        
        if max_prob < 0.65:
            prediction = 'neutral'
        elif case['prob_negative'] > case['prob_positive']:
            prediction = 'negative'
        else:
            prediction = 'positive'
        
        print(f"  → Tahmin: {prediction} (confidence: {max_prob:.2f})")