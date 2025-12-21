import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, StatusBar, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { login } from '../services/ApiService'; // login fonksiyonunu import et

export default function LoginScreen() {
  const navigation = useNavigation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Hata', 'Lütfen e-posta ve şifrenizi girin.');
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      // Başarılı giriş sonrası ana sayfaya yönlendir
      navigation.reset({
        index: 0,
        routes: [{ name: 'Main' }],
      });
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
        <Ionicons name="time-outline" size={48} color={COLORS.accent} style={styles.logo} />
        
        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor={COLORS.text_tertiary}
          keyboardType="email-address"
          autoCapitalize="none"
          value={email}
          onChangeText={setEmail}
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
        
        <TouchableOpacity onPress={handleLogin} style={styles.buttonContainer} disabled={loading}>
          <LinearGradient
            colors={[COLORS.primary, COLORS.accent]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.button}
          >
            <Text style={styles.buttonText}>{loading ? 'Logging In...' : 'Log In'}</Text>
          </LinearGradient>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
          <Text style={styles.footerText}>
            Don't have an account?{' '}
            <Text style={styles.linkText}>Sign Up</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

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
    overflow: 'hidden', // Gradient'in taşmasını engeller
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