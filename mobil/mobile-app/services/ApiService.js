import { Alert, Keyboard } from 'react-native';


const API_URL = 'http://192.168.110.192:8000'; 


export const kaydet = async (metin, setLoading, setMetin, navigation) => {
  if (!metin.trim()) {
    Alert.alert('Hata', 'Lütfen bir metin giriniz.');
    return;
  }

  setLoading(true);
  Keyboard.dismiss();

  try {
    // A. Önce Kaydet
    const response = await fetch(`${API_URL}/entries`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ metin: metin }),
    });

    const json = await response.json();

    if (!response.ok) {
        throw new Error(json.detail || 'Sunucu hatası oluştu.');
    }

    if (json.status === 'success') {
      const entryId = json.data.id; // Yeni kaydedilen günlüğün ID'si
      
      // B. Kayıt Başarılıysa Hemen AI Tahminini Sor (Zincirleme İstek)
      try {
          const predictResponse = await fetch(`${API_URL}/predict-mood/${entryId}`);
          const predictJson = await predictResponse.json();
          
          if (predictResponse.ok) {
              const { mood_score, emoji, message } = predictJson.ai_prediction;
              
              // C. Kullanıcıya Havalı Bir Sonuç Göster
              Alert.alert(
                  `AI Analizi: ${emoji}`,
                  `Mod Puanın: ${mood_score}/5\n\n${message}`,
                  [
                      { 
                          text: 'Süper!', 
                          onPress: () => {
                              setMetin(''); // Temizle
                              // Eğer navigation prop'u geldiyse Ana Sayfaya dön
                              if (navigation) navigation.navigate('Home'); 
                          }
                      }
                  ]
              );
          } else {
              // Tahmin alınamazsa sadece başarı mesajı ver
              throw new Error("Tahmin alınamadı");
          }
      } catch (predictError) {
          // Tahmin servisi çalışmazsa bile kayıt başarılıdır, kullanıcıyı üzme
          Alert.alert('Başarılı', 'Günlüğün kaydedildi!', [
              { text: 'Tamam', onPress: () => {
                  setMetin('');
                  if (navigation) navigation.navigate('Home');
              }}
          ]);
      }
      
    } else {
      throw new Error(json.message || 'Beklenmedik bir cevap geldi.');
    }
  } catch (error) {
    console.error(error);
    Alert.alert('Hata', error.message || 'Sunucuya bağlanılamadı.');
  } finally {
    setLoading(false);
  }
};

// 2. GEÇMİŞ GÜNLÜKLERİ LİSTELEME (Ana Sayfa ve Listeler İçin)
export const fetchEntries = async () => {
    try {
        // Son 50 kaydı getir
        const response = await fetch(`${API_URL}/entries?limit=50`);
        if (!response.ok) {
            console.error("Veri çekme hatası:", await response.text());
            return [];
        }
        return await response.json();
    } catch (error) {
        console.error("Fetch hatası (Bağlantı yok mu?):", error);
        return [];
    }
};

// 3. TEKİL TAHMİN SORGULAMA (Detay Sayfası İçin - Opsiyonel)
export const getMoodPrediction = async (entryId) => {
    try {
        const response = await fetch(`${API_URL}/predict-mood/${entryId}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        return null;
    }
};

export const fetchDailyInsight = async () => {
    try {
        const response = await fetch(`${API_URL}/insights`);
        if (!response.ok) return null;
        
        // DÜZELTME: json.insight diyerek sadece metni almak yerine
        // TÜM OBJEYİ döndürüyoruz (içinde insight, trend, related_topic var)
        return await response.json(); 
        
    } catch (error) {
        console.log("Insight hatası:", error);
        // Hata durumunda da obje dönüyoruz ki ekran bozulmasın
        return { insight: "Bugün harika bir gün olabilir!", trend: "neutral" };
    }
};