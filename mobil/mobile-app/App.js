import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';

export default function App() {
  // Gelen mesajı ve yüklenme durumunu saklamak için state'ler
  const [mesaj, setMesaj] = useState('');
  const [loading, setLoading] = useState(true);

  // Bu fonksiyon component ekrana ilk geldiğinde bir kere çalışır
  useEffect(() => {
    // KENDİ IP ADRESİNİ YAZMAYI UNUTMA!
    fetch('http://192.168.192.155:8000') // ÖRNEK IP, BURAYI DEĞİŞTİR
      .then((response) => response.json())
      .then((json) => setMesaj(json.mesaj)) // Gelen JSON'daki "mesaj" alanını al
      .catch((error) => {
        console.error(error);
        setMesaj('Bağlantı Hatası!'); // Hata olursa bunu yaz
      })
      .finally(() => setLoading(false)); // Her durumda yüklenmeyi bitir
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Lumos TEXT'ten Gelen Mesaj:</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <Text style={styles.message}>{mesaj}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  message: {
    fontSize: 24,
    color: 'green',
  },
});