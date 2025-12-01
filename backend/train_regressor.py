# train_regressor.py (GÜNCELLENMİŞ - METRİKLİ)

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# --- 1. VERİ YÜKLEME ---
try:
    train_df = pd.read_csv('train_data.csv')
    val_df = pd.read_csv('val_data.csv')
except FileNotFoundError:
    print("❌ Dosyalar bulunamadı.")
    exit(1)

# --- 2. HEDEF VE ÖZELLİKLER ---
TARGET_COLUMN = 'user_mood'

X_train = train_df.drop(columns=[TARGET_COLUMN, 'duygu_label'])
y_train = train_df[TARGET_COLUMN]
X_val = val_df.drop(columns=[TARGET_COLUMN, 'duygu_label'])
y_val = val_df[TARGET_COLUMN]
FEATURES = X_train.columns.tolist()

# --- 3. EĞİTİM ---
print("\n🚀 Model Eğitiliyor...")
model = RandomForestRegressor(
    random_state=42, 
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=2
)
model.fit(X_train, y_train)

# --- 4. DEĞERLENDİRME (DETAYLI METRİKLER) ---
print("📊 Değerlendiriliyor...")
y_pred = model.predict(X_val)

# Temel Hata Metrikleri
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
mae = mean_absolute_error(y_val, y_pred)

# R-Kare (Modelin veriyi açıklama gücü - % olarak düşünülebilir)
r2 = r2_score(y_val, y_pred)

# ÖZEL DOĞRULUK (Custom Accuracy)
# Mantık: Eğer tahmin, gerçek değerden en fazla 0.5 puan şaştıysa "DOĞRU" kabul et.
# Örn: Gerçek 4, Tahmin 4.4 -> DOĞRU. Gerçek 4, Tahmin 3.2 -> YANLIŞ.
threshold = 0.5
correct_predictions = np.sum(np.abs(y_val - y_pred) <= threshold)
custom_accuracy = (correct_predictions / len(y_val)) * 100

print(f"\n🏆 MODEL PERFORMANS RAPORU")
print(f"==========================================")
print(f"1. Ortalama Sapma (MAE): {mae:.4f}")
print(f"   (Model ortalama {mae:.2f} puan hata yapıyor)")
print(f"------------------------------------------")
print(f"2. Açıklayıcılık Oranı (R2 Score): {r2:.4f}")
print(f"   (Model verideki değişimin %{r2*100:.1f}'ini açıklayabiliyor)")
print(f"------------------------------------------")
print(f"3. Toleranslı Doğruluk (±0.5 Puan): %{custom_accuracy:.2f}")
print(f"   (Tahminlerin %{custom_accuracy:.1f}'i, gerçek puana çok yakın)")
print(f"==========================================")

print("\n👀 Örnek Tahminler:")
results = pd.DataFrame({'Gerçek': y_val, 'Tahmin': np.round(y_pred, 1)})
print(results.head(5))

# --- 5. KAYIT ---
model_filename = 'mood_regressor.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump({'model': model, 'features': FEATURES}, f)
print(f"\n✅ Model kaydedildi: {model_filename}")