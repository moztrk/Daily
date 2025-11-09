# train_regressor.py

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# --- 1. VERİ YÜKLEME ---

try:
    train_df = pd.read_csv('train_data.csv')
    val_df = pd.read_csv('val_data.csv')
except FileNotFoundError:
    print("❌ HATA: train_data.csv veya val_data.csv bulunamadı.")
    print("💡 Önce 'python prepare_data.py' script'ini çalıştırdığınızdan emin olun.")
    exit(1)

print(f"✓ Train verisi yüklendi: {train_df.shape}")
print(f"✓ Validation verisi yüklendi: {val_df.shape}")

# --- 2. HEDEF (y) VE ÖZELLİKLER (X) BELİRLEME ---

# YENİ HEDEF: 'duygu_skoru' (sayısal değer)
TARGET_COLUMN = 'duygu_skoru'

# Özellikler (X): Hedef sütun VE onunla ilişkili 'duygu_label' dışındaki her şey
try:
    X_train = train_df.drop(columns=[TARGET_COLUMN, 'duygu_label'])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN, 'duygu_label'])
    y_val = val_df[TARGET_COLUMN]
    
    # Modelin hangi sütunlara bakarak öğrendiğini kaydet
    FEATURES = X_train.columns.tolist()
    
except KeyError:
    print(f"❌ HATA: '{TARGET_COLUMN}' veya 'duygu_label' sütunu veride bulunamadı.")
    exit(1)

print(f"✓ Model, {len(FEATURES)} adet özellik (feature) kullanarak eğitilecek.")
print(f"🎯 Hedef Sütun (Tahmin): {TARGET_COLUMN}")

# --- 3. MODELİ TANIMLAMA VE EĞİTME ---

# İş paketinde istenen model
model = RandomForestRegressor(
    random_state=42, 
    n_estimators=150,      # Ormandaki ağaç sayısı
    max_depth=10,          # Ağaçların maksimum derinliği
    min_samples_leaf=5     # Bir yapraktaki minimum örnek (ezberlemeyi önler)
)

print("\n" + "="*60)
print(f"🚀 {type(model).__name__} EĞİTİMİ BAŞLIYOR...")
print("="*60)

# Modeli eğit
print("   ⏳ Eğitiliyor...")
model.fit(X_train, y_train)

# --- 4. DEĞERLENDİRME (REGRESYON METRİKLERİ) ---

print("   📊 Değerlendiriliyor (Validation Set)...")
y_pred = model.predict(X_val)

# RMSE (Root Mean Squared Error) kullanalım.
# Bu, modelin tahminlerinin ortalama ne kadar "saptığını" gösterir.
# 0'a ne kadar yakınsa o kadar iyidir.
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)

print(f"\n   🎯 Kök Ortalama Kare Hata (RMSE): {rmse:.4f}")
print("       (Bu değerin 0'a yakın olması modelin iyi olduğunu gösterir)")

# Gerçek ve Tahmini değerlerden birkaç örnek göster
print("\n   Örnek Tahminler (Gerçek vs. Tahmin):")
comparison_df = pd.DataFrame({'Gerçek Skor': y_val, 'Tahmin Edilen Skor': y_pred})
print(comparison_df.head())

# --- 5. MODELİ KAYDETME ---

model_filename = 'mood_regressor.pkl'
# Özellik listesini ve modeli tek bir dosyaya kaydet
model_payload = {
    'model': model,
    'features': FEATURES
}

with open(model_filename, 'wb') as f:
    pickle.dump(model_payload, f)
    
print("\n" + "="*60)
print("✅ EĞİTİM TAMAMLANDI!")
print(f"🏆 Regresyon modeli '{model_filename}' olarak kaydedildi.")
print("="*60)