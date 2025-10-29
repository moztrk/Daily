// services/ApiService.js
import { Alert, Keyboard } from 'react-native';

// API_URL'i de buraya taşıdık.
const API_URL = 'http://192.168.118.5:8000'; // Kendi IP adresin

export const kaydet = async (metin, setLoading, setMetin) => {
  if (!metin.trim()) {
    Alert.alert('Hata', 'Lütfen bir metin giriniz.');
    return;
  }

  setLoading(true);
  Keyboard.dismiss();

  try {
    const response = await fetch(`${API_URL}/entries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ metin: metin }),
    });

    const json = await response.json();

    if (!response.ok) {
        // FastAPI'den gelen 'detail' mesajını yakala
        const errorMessage = json.detail || 'Bilinmeyen bir sunucu hatası oluştu.';
        throw new Error(errorMessage);
    }

    if (json.status === 'success') {
      Alert.alert('Başarılı', 'Girdiniz başarıyla kaydedildi!');
      setMetin(''); // Metin kutusunu temizle
      
      // TODO: Başarılı kayıttan sonra Ana Sayfa'ya yönlendir
      // navigation.navigate('Home');
      
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