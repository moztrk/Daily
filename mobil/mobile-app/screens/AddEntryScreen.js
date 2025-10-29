// screens/AddEntryScreen.js
import React from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Keyboard, StatusBar } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS } from '../constants/colors';
import { kaydet } from '../services/ApiService'; // API fonksiyonunu import et

export default function AddEntryScreen() {
  const [metin, setMetin] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleKaydet = () => {
    // API servisini çağır, state'leri ona yolla
    kaydet(metin, setLoading, setMetin);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.content}>
        <Text style={styles.title}>Bugün Nasılsın?</Text>
        <TextInput
          style={styles.input}
          placeholder="Bugün olanları, hissettiklerini buraya yaz..."
          placeholderTextColor={COLORS.text_tertiary}
          multiline={true}
          value={metin}
          onChangeText={setMetin}
          textAlignVertical="top"
        />
        <TouchableOpacity
          style={[styles.buttonContainer, loading && styles.buttonDisabled]}
          onPress={handleKaydet}
          disabled={loading}
        >
          <LinearGradient
            colors={loading ? [COLORS.card_elevated, COLORS.card_elevated] : [COLORS.primary, COLORS.accent]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.button}
          >
            <Text style={styles.buttonText}>{loading ? 'Kaydediliyor...' : 'Kaydet'}</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// Stilleri yeni tasarıma göre güncelledik
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'flex-start', // İçeriği üste al
    paddingTop: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text_primary,
    marginBottom: 24,
  },
  input: {
    flex: 1, // Alanı genişlet
    maxHeight: '50%', // Ekranın yarısını kaplasın
    backgroundColor: COLORS.card,
    color: COLORS.text_primary,
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    marginBottom: 24,
    borderColor: COLORS.card_elevated,
    borderWidth: 1,
  },
  buttonContainer: {
    borderRadius: 8,
    overflow: 'hidden',
  },
  button: {
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});