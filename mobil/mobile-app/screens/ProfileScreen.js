import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { logout } from '../services/ApiService';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function ProfileScreen({ navigation }) {
  const [userEmail, setUserEmail] = useState('Yükleniyor...');

  useEffect(() => {
    // Kullanıcı bilgilerini AsyncStorage'dan çek
    const loadUserInfo = async () => {
      try {
        const email = await AsyncStorage.getItem('userEmail');
        if (email) {
          setUserEmail(email);
        }
      } catch (e) {
        console.error("Kullanıcı bilgisi yüklenemedi", e);
      }
    };
    loadUserInfo();
  }, []);

  const handleLogout = () => {
      Alert.alert("Çıkış Yap", "Hesabından çıkmak istediğine emin misin?", [
          { text: "İptal", style: "cancel" },
          { text: "Çıkış Yap", style: "destructive", onPress: () => logout(navigation) }
      ]);
  };

  const MenuItem = ({ icon, title, isDestructive = false, onPress }) => (
      <TouchableOpacity style={styles.menuItem} onPress={onPress}>
          <View style={styles.menuIconContainer}>
              <Ionicons name={icon} size={22} color={isDestructive ? COLORS.negative : COLORS.text_primary} />
          </View>
          <Text style={[styles.menuText, isDestructive && { color: COLORS.negative }]}>{title}</Text>
          <Ionicons name="chevron-forward" size={20} color={COLORS.text_tertiary} />
      </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={{ padding: 20 }}>
        
        {/* Profil Başlığı */}
        <View style={styles.profileHeader}>
            <View style={styles.avatarContainer}>
                {/* Rastgele bir avatar yerine placeholder veya e-posta baş harfi kullanılabilir */}
                <Image 
                    source={{ uri: 'https://i.pravatar.cc/150?img=12' }} 
                    style={styles.avatar} 
                />
                <View style={styles.editBadge}>
                    <Ionicons name="pencil" size={12} color="#FFF" />
                </View>
            </View>
            <Text style={styles.name}>Kullanıcı</Text>
            <Text style={styles.email}>{userEmail}</Text>
        </View>

        {/* Menü */}
        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Hesap Ayarları</Text>
            <MenuItem icon="person-circle-outline" title="Kişisel Bilgiler" />
            <MenuItem icon="notifications-outline" title="Bildirimler" />
            <MenuItem icon="lock-closed-outline" title="Gizlilik ve Güvenlik" />
        </View>

        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Uygulama</Text>
            <MenuItem icon="help-circle-outline" title="Yardım ve Destek" />
            <MenuItem icon="information-circle-outline" title="Hakkında" />
        </View>

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Text style={styles.logoutText}>Çıkış Yap</Text>
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  
  profileHeader: { alignItems: 'center', marginBottom: 32, marginTop: 16 },
  avatarContainer: { position: 'relative', marginBottom: 16 },
  avatar: { width: 100, height: 100, borderRadius: 50, borderWidth: 3, borderColor: COLORS.primary },
  editBadge: { 
      position: 'absolute', bottom: 0, right: 0, 
      backgroundColor: COLORS.accent, padding: 6, borderRadius: 20, 
      borderWidth: 2, borderColor: COLORS.background 
  },
  name: { fontSize: 24, fontWeight: 'bold', color: COLORS.text_primary },
  email: { fontSize: 14, color: COLORS.text_tertiary, marginTop: 4 },

  section: { marginBottom: 24 },
  sectionTitle: { fontSize: 14, color: COLORS.text_tertiary, marginBottom: 8, marginLeft: 4, textTransform: 'uppercase' },
  
  menuItem: { 
      flexDirection: 'row', alignItems: 'center', 
      backgroundColor: COLORS.card, padding: 16, borderRadius: 12, marginBottom: 8 
  },
  menuIconContainer: { width: 32 },
  menuText: { flex: 1, fontSize: 16, color: COLORS.text_primary, fontWeight: '500' },

  logoutButton: { 
      backgroundColor: 'rgba(248, 113, 113, 0.1)', 
      padding: 16, borderRadius: 12, alignItems: 'center', marginTop: 8 
  },
  logoutText: { color: COLORS.negative, fontWeight: 'bold', fontSize: 16 }
});