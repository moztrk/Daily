import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, StatusBar, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { signUp } from '../services/ApiService'; // signUp fonksiyonunu import et

export default function SignUpScreen() {
  const navigation = useNavigation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignUp = async () => {
    if (!email || !password || !confirmPassword) {
      Alert.alert('Hata', 'Lütfen tüm alanları doldurun.');
      return;
    }

    if (password !== confirmPassword) {
      Alert.alert('Hata', 'Şifreler uyuşmuyor.');
      return;
    }

    setLoading(true);
    try {
      await signUp(email, password);
      Alert.alert('Başarılı', 'Kayıt işlemi başarılı! Lütfen giriş yapın.', [
        { text: 'Tamam', onPress: () => navigation.navigate('Login') }
      ]);
    } catch (error) {
      // Hata zaten ApiService içinde gösteriliyor
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.content}>
        
        <Ionicons name="checkmark-circle-outline" size={48} color={COLORS.accent} style={styles.logo} />
        <Text style={styles.title}>Create Your Account</Text>

        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor={COLORS.text_tertiary}
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
        />
        
        <Text style={styles.label}>Password</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your password"
          placeholderTextColor={COLORS.text_tertiary}
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <Text style={styles.label}>Confirm Password</Text>
        <TextInput
          style={styles.input}
          placeholder="Confirm your password"
          placeholderTextColor={COLORS.text_tertiary}
          secureTextEntry
          value={confirmPassword}
          onChangeText={setConfirmPassword}
        />
        
        <TouchableOpacity style={styles.buttonContainer} onPress={handleSignUp} disabled={loading}>
          <LinearGradient
            colors={[COLORS.primary, COLORS.accent]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.button}
          >
            <Text style={styles.buttonText}>{loading ? 'Signing Up...' : 'Sign Up'}</Text>
          </LinearGradient>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={() => navigation.navigate('Login')}>
          <Text style={styles.footerText}>
            Already have an account?{' '}
            <Text style={styles.linkText}>Log In</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// LoginScreen'deki stillerin aynısını kullanıyoruz (pratikte bunları tek bir dosyadan alırsın)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  logo: {
    alignSelf: 'center',
    marginBottom: 16,
  },
  title: {
    color: COLORS.text_primary,
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 32,
  },
  label: {
    color: COLORS.text_primary,
    fontSize: 16,
    fontWeight: '500',
    marginBottom: 8,
  },
  input: {
    backgroundColor: COLORS.card,
    color: COLORS.text_primary,
    height: 56,
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    borderColor: COLORS.card_elevated,
    borderWidth: 1,
    marginBottom: 20,
  },
  buttonContainer: {
    marginTop: 16,
    borderRadius: 8,
    overflow: 'hidden',
  },
  button: {
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  footerText: {
    color: COLORS.text_secondary,
    textAlign: 'center',
    marginTop: 24,
    fontSize: 14,
  },
  linkText: {
    color: COLORS.accent,
    fontWeight: 'bold',
  },
});