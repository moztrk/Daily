# train_binary_model.py - BINARY CLASSIFICATION (Negative vs Positive)

import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import warnings

warnings.filterwarnings('ignore')

# --- VERİ YÜKLEME ---
try:
    train_df = pd.read_csv('train_data.csv')
    val_df = pd.read_csv('val_data.csv')
except FileNotFoundError:
    print("❌ train_data.csv veya val_data.csv bulunamadı.")
    exit(1)

print(f"✓ Train: {train_df.shape}")
print(f"✓ Validation: {val_df.shape}")

# --- BINARY LABEL OLUŞTUR ---
# Strateji: Negative (-1) vs Non-Negative (0, 1)
def convert_to_binary(label):
    """
    -1 (Negative) → 0
    0, 1 (Neutral, Positive) → 1
    """
    return 0 if label == -1 else 1

train_df['binary_label'] = train_df['duygu_label'].apply(convert_to_binary)
val_df['binary_label'] = val_df['duygu_label'].apply(convert_to_binary)

# Dağılımı kontrol et
print(f"\n📊 Binary Label Dağılımı (Train):")
print(train_df['binary_label'].value_counts())
print(f"\n📊 Binary Label Dağılımı (Validation):")
print(val_df['binary_label'].value_counts())

# --- X VE Y AYIR ---
X_train = train_df.drop(columns=['duygu_label', 'duygu_skoru', 'binary_label'])
y_train = train_df['binary_label']

X_val = val_df.drop(columns=['duygu_label', 'duygu_skoru', 'binary_label'])
y_val = val_df['binary_label']

FEATURES = X_train.columns.tolist()
print(f"\n✓ Model, {len(FEATURES)} feature kullanacak.")

# --- MODEL TANIMLAMA ---
models = {
    "Logistic Regression": LogisticRegression(
        random_state=42,
        class_weight='balanced',
        max_iter=2000,
        C=0.5
    ),
    "Random Forest": RandomForestClassifier(
        random_state=42,
        class_weight='balanced',
        n_estimators=100,
        max_depth=10,
        min_samples_leaf=5
    )
}

best_model = None
best_f1 = -1.0

print("\n" + "="*60)
print("🚀 BINARY CLASSIFICATION EĞİTİMİ")
print("="*60)

# --- EĞİTİM ---
for name, model in models.items():
    print(f"\n--- Model: {name} ---")
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    
    accuracy = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred, average='binary')
    
    print(f"   ✅ Accuracy: {accuracy:.4f}")
    print(f"   🎯 F1 Score: {f1:.4f}")
    
    print("\n   Detaylı Rapor:")
    report = classification_report(
        y_val, y_pred,
        target_names=['Negative', 'Non-Negative (Neutral+Positive)']
    )
    print(report)
    
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        print(f"   ⭐ YENİ EN İYİ MODEL!")

# --- KAYDET ---
print("\n" + "="*60)
print("✅ EĞİTİM TAMAMLANDI!")
print("="*60)

if best_model:
    model_payload = {
        'model': best_model,
        'features': FEATURES,
        'model_type': 'binary'  # Binary olduğunu işaretle
    }
    
    with open('sentiment_binary_model.pkl', 'wb') as f:
        pickle.dump(model_payload, f)
    
    print(f"🏆 En iyi model kaydedildi: sentiment_binary_model.pkl")
    print(f"   Model: {type(best_model).__name__}")
    print(f"   F1 Score: {best_f1:.4f}")
    print(f"\n💡 Bu model 2 sınıf tahmin eder:")
    print("   0: Negative (Kötü)")
    print("   1: Non-Negative (Nötr veya İyi)")