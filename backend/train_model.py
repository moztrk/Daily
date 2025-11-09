# train_model.py

import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import warnings

# Uyarıları gizle (model eğitiminde çok fazla uyarı çıkabilir)
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

# Hedefimiz: 'duygu_label' (-1, 0, 1) sütununu tahmin etmek
TARGET_COLUMN = 'duygu_label'

# Özellikler (X): Hedef sütun dışındaki her şey
# 'duygu_skoru'nu da çıkarıyoruz, çünkü bu hedefle doğrudan ilişkili (kopya olur)
try:
    X_train = train_df.drop(columns=[TARGET_COLUMN, 'duygu_skoru'])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN, 'duygu_skoru'])
    y_val = val_df[TARGET_COLUMN]
    
    # Modelin hangi sütunlara bakarak öğrendiğini kaydet (sonraki adım için)
    FEATURES = X_train.columns.tolist()
    
except KeyError:
    print(f"❌ HATA: '{TARGET_COLUMN}' veya 'duygu_skoru' sütunu veride bulunamadı.")
    exit(1)

print(f"✓ Model, {len(FEATURES)} adet özellik (feature) kullanarak eğitilecek.")

# --- 3. DENGESİZ VERİ İÇİN AĞIRLIKLANDIRMA (ÖNEMLİ!) ---
# Loglardan gördüğümüz kadarıyla negatif (125) > pozitif (80) > nötr (38)
# Bu, modelin 'negatif'e ağırlık vermesini sağlar.
weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = dict(zip(np.unique(y_train), weights))

print(f"✓ Dengesiz veri tespiti: Sınıf ağırlıkları hesaplandı: {class_weights}")


# --- 4. MODELLERİ TANIMLAMA ---

models = {
    "Logistic Regression": LogisticRegression(
        random_state=42, 
        class_weight=class_weights, # Dengeleme
        max_iter=1000
    ),
    "Random Forest": RandomForestClassifier(
        random_state=42, 
        class_weight=class_weights, # Dengeleme
        n_estimators=100 # 100 ağaçlı bir orman
    ),
    "SVM (Linear)": SVC(
        random_state=42, 
        class_weight=class_weights, # Dengeleme
        kernel='linear',
        probability=True
    )
}

best_model = None
best_f1_score = -1.0 # En iyi skoru takip et

print("\n" + "="*60)
print("🚀 MODEL EĞİTİMİ VE DEĞERLENDİRMESİ BAŞLIYOR...")
print("="*60)

# --- 5. EĞİTİM VE DEĞERLENDİRME DÖNGÜSÜ ---

for name, model in models.items():
    print(f"\n--- Model: {name} ---")
    
    # Modeli eğit
    print("   ⏳ Eğitiliyor...")
    model.fit(X_train, y_train)
    
    # Validation verisi üzerinde tahmin yap
    print("   📊 Değerlendiriliyor (Validation Set)...")
    y_pred = model.predict(X_val)
    
    # Raporları yazdır
    accuracy = accuracy_score(y_val, y_pred)
    # 'macro' F1 skoru, dengesiz sınıflar için en adil başarı ölçütüdür
    f1 = f1_score(y_val, y_pred, average='macro')
    
    print(f"   ✅ Doğruluk (Accuracy): {accuracy:.4f}")
    print(f"   🎯 F1 Skoru (Macro): {f1:.4f}")
    
    print("\n   Sınıflandırma Raporu (Validation):")
    # precision, recall, f1-score detayları
    report = classification_report(y_val, y_pred, target_names=['Negative (-1)', 'Neutral (0)', 'Positive (1)'])
    print(report)
    
    # En iyi modeli güncelle
    if f1 > best_f1_score:
        best_f1_score = f1
        best_model = model
        print(f"   ⭐ YENİ EN İYİ MODEL! ({name})")

# --- 6. EN İYİ MODELİ KAYDETME ---

print("\n" + "="*60)
print("✅ EĞİTİM TAMAMLANDI!")
print("="*60)

if best_model:
    model_filename = 'sentiment_model.pkl'
    # Özellik listesini ve modeli tek bir dosyaya kaydet
    model_payload = {
        'model': best_model,
        'features': FEATURES
    }
    
    with open(model_filename, 'wb') as f:
        pickle.dump(model_payload, f)
        
    print(f"🏆 En iyi model ({type(best_model).__name__}) '{model_filename}' olarak kaydedildi.")
    print(f"   En iyi F1 Skoru (Macro): {best_f1_score:.4f}")
else:
    print("❌ HATA: Hiçbir model başarıyla eğitilemedi.")

print("\n🎯 Sonraki adım: 'test_data.csv' ile final testi yapmak veya API'ye entegre etmek.")