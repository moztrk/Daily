import { Alert, Keyboard } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://192.168.110.192:8000'; 


// --- AUTH İŞLEMLERİ ---

// Token'ı alan yardımcı fonksiyon
const getAuthHeaders = async () => {
    const token = await AsyncStorage.getItem('userToken');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

// 1. Kayıt Ol (Sign Up)
export const signUp = async (email, password) => {
    try {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        
        const json = await response.json();
        
        if (!response.ok) {
            throw new Error(json.detail || 'Kayıt başarısız.');
        }
        
        return json; // { msg: "Kayıt başarılı", user: ... }
    } catch (error) {
        Alert.alert('Hata', error.message);
        throw error;
    }
};

// 2. Giriş Yap (Login)
export const login = async (email, password) => {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        
        const json = await response.json();
        
        if (!response.ok) {
            throw new Error(json.detail || 'Giriş başarısız.');
        }
        
        // Token ve User bilgilerini sakla
        await AsyncStorage.setItem('userToken', json.access_token);
        await AsyncStorage.setItem('userId', String(json.user.id));
        await AsyncStorage.setItem('userEmail', json.user.email);
        
        return json;
    } catch (error) {
        Alert.alert('Hata', error.message);
        throw error;
    }
};

// 3. Çıkış Yap (Logout)
export const logout = async (navigation) => {
    try {
        await AsyncStorage.clear();
        navigation.reset({
            index: 0,
            routes: [{ name: 'Login' }],
        });
    } catch (e) {
        console.error("Çıkış hatası:", e);
    }
};

// --- GÜNCELLENMİŞ FONKSİYONLAR (Token ile İstek Atma) ---

export const kaydet = async (metin, setLoading, setMetin, navigation) => {
  if (!metin.trim()) {
    Alert.alert('Hata', 'Lütfen bir metin giriniz.');
    return;
  }

  setLoading(true);
  Keyboard.dismiss();

  try {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_URL}/entries`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ metin: metin }),
    });

    const json = await response.json();

    if (!response.ok) {
        throw new Error(json.detail || 'Sunucu hatası oluştu.');
    }

    if (json.status === 'success') {
      const entryId = json.data.id;
      
      try {
          const predictResponse = await fetch(`${API_URL}/predict-mood/${entryId}`, { headers });
          const predictJson = await predictResponse.json();
          
          if (predictResponse.ok) {
              const { mood_score, emoji, message } = predictJson.ai_prediction;
              
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

export const fetchEntries = async () => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_URL}/entries?limit=50`, { headers });
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

export const getMoodPrediction = async (entryId) => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_URL}/predict-mood/${entryId}`, { headers });
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        return null;
    }
};

export const fetchDailyInsight = async () => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_URL}/insights`, { headers });
        if (!response.ok) return null;
        
        return await response.json(); 
        
    } catch (error) {
        console.log("Insight hatası:", error);
        return { insight: "Bugün harika bir gün olabilir!", trend: "neutral" };
    }
};