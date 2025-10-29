import React from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert, Keyboard } from 'react-native';

export default function App() {
  // Kullanıcının yazdığı metni tutmak için state
  const [metin, setMetin] = React.useState('');
  // Kaydetme işlemi sırasında butonu pasif yapmak için state
  const [loading, setLoading] = React.useState(false);

  
  const API_URL = 'http://192.168.118.5:8000'; 

  const kaydet = async () => {
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
        // Backend'deki Pydantic modeline uygun JSON gönder
        body: JSON.stringify({ metin: metin }),
      });

      const json = await response.json();

      if (json.status === 'success') {
        Alert.alert('Başarılı', 'Girdiniz başarıyla kaydedildi!');
        setMetin(''); // Metin kutusunu temizle
      } else {
        Alert.alert('Hata', `Bir sorun oluştu: ${json.message}`);
      }
    } catch (error) {
      console.error(error);
      Alert.alert('Bağlantı Hatası', 'Sunucuya bağlanılamadı. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bugün Nasılsın?</Text>
      <TextInput
        style={styles.input}
        placeholder="Bugün olanları buraya yaz..."
        multiline={true}
        value={metin}
        onChangeText={setMetin} // Yazılan her karakterde 'metin' state'ini güncelle
      />
      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={kaydet}
        disabled={loading} // Yükleme sırasında butonu devre dışı bırak
      >
        <Text style={styles.buttonText}>{loading ? 'Kaydediliyor...' : 'Kaydet'}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 150,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    textAlignVertical: 'top', // Metnin yukarıdan başlamasını sağlar
    fontSize: 16,
    marginBottom: 20,
  },
  button: {
    width: '100%',
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#a9a9a9',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});