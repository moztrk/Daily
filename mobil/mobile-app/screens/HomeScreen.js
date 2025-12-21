/**
 * HomeScreen - Geliştirilmiş Versiyon
 * 
 * ÖZELLİKLER:
 * ✅ Akıllı Motivasyon Kartı (3 farklı durum mesajı)
 * ✅ Haftalık Mood Takvimi (7 günlük emoji görsel)
 * ✅ Hızlı İstatistikler (Pozitiflik oranı, en çok yazılan konu)
 * ✅ Interaktif günler (tıklanabilir)
 * ❌ AI İçgörü kartı kaldırıldı
 */

import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { fetchEntries } from '../services/ApiService';

export default function HomeScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({ streak: 0, total: 0, lastMood: 0 });

  /**
   * Ana veri yükleme fonksiyonu
   * Son 50 günlüğü çeker (haftalık takvim için yeterli)
   */
  const loadData = async () => {
    setRefreshing(true);

    try {
        const data = await fetchEntries();
        setEntries(data);
        
        if (data.length > 0) {
            const lastEntry = data[0];
            const sentiment = lastEntry.analiz_sonucu?.sentiment?.skor || 0;
            setStats({
                streak: calculateStreak(data),
                total: data.length,
                lastMood: sentiment
            });
        }
    } catch (e) {
        console.log(e);
    } finally {
        setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadData();
    }, [])
  );

  /**
   * Seri hesaplama (ardışık günler)
   * Gerçek uygulama: tarih farkı 1 gün olmalı
   */
  const calculateStreak = (data) => {
      if (data.length === 0) return 0;
      
      let streak = 1;
      const today = new Date().setHours(0, 0, 0, 0);
      
      for (let i = 0; i < data.length - 1; i++) {
          const currentDate = new Date(data[i].created_at).setHours(0, 0, 0, 0);
          const nextDate = new Date(data[i + 1].created_at).setHours(0, 0, 0, 0);
          
          const diffDays = (currentDate - nextDate) / (1000 * 60 * 60 * 24);
          
          if (diffDays === 1) {
              streak++;
          } else {
              break;
          }
      }
      
      return Math.min(streak, 7);
  };

  /**
   * Bugün yazıldı mı kontrolü
   */
  const checkTodayEntry = () => {
    if (entries.length === 0) return null;
    
    const today = new Date().setHours(0, 0, 0, 0);
    const todayEntry = entries.find(e => {
      const entryDate = new Date(e.created_at).setHours(0, 0, 0, 0);
      return entryDate === today;
    });
    
    return todayEntry;
  };

  /**
   * Son yazma tarihinden bu yana geçen gün sayısı
   */
  const getDaysSinceLastEntry = () => {
    if (entries.length === 0) return 0;
    
    const today = new Date();
    const lastEntryDate = new Date(entries[0].created_at);
    const diffTime = Math.abs(today - lastEntryDate);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
  };

  /**
   * Motivasyon kartı verisi oluştur
   */
  const getMotivationCard = () => {
    const todayEntry = checkTodayEntry();
    const daysSinceLastEntry = getDaysSinceLastEntry();
    const isFirstTime = entries.length === 0;

    // Durum 1: İlk kez kullanıcı
    if (isFirstTime) {
      return {
        type: 'welcome',
        icon: 'rocket',
        iconColor: '#3B82F6',
        borderColor: '#3B82F6',
        title: 'Hoş Geldin! 🎉',
        message: 'Günlük tutmak, zihinsel sağlığını iyileştirmenin en etkili yollarından biri. Hadi başlayalım!',
        showButton: false
      };
    }

    // Durum 2: Bugün zaten yazdı
    if (todayEntry) {
      return {
        type: 'completed',
        icon: 'checkmark-circle',
        iconColor: '#10B981',
        borderColor: '#10B981',
        title: 'Harika! ✨',
        message: 'Bugün günlüğünü yazdın. Düzenli yazmaya devam et!',
        showButton: true,
        buttonText: 'Son Yazdıklarını Gör',
        buttonAction: () => navigation.navigate('Entries')  // ✅ DÜZELTİLDİ: 'Journal' → 'Entries'
      };
    }

    // Durum 3: Bugün yazmadı
    const quotes = [
      '"Yazı yazmak, düşünceleri netleştirmenin en güçlü yoludur."',
      '"Her gün kendine birkaç dakika ayır, yarın sana teşekkür edecek."',
      '"Duyguları yazmak, onları anlamlandırmanın ilk adımıdır."',
      '"Küçük adımlar büyük değişimlere yol açar."'
    ];
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

    return {
      type: 'reminder',
      icon: 'time',
      iconColor: '#F59E0B', // Turuncu
      borderColor: '#F59E0B',
      title: daysSinceLastEntry === 0 ? 'Bugün Henüz Yazmadın' : `${daysSinceLastEntry} Gündür Yazmadın`,
      message: daysSinceLastEntry === 0 
        ? 'Bugün nasıl hissettiğini paylaşmak ister misin?' 
        : `Son ${daysSinceLastEntry} gündür yazmadın. Bugün nasıl hissettiğini paylaşmak ister misin?`,
      showButton: false,
      quote: randomQuote
    };
  };

  /**
   * Son 7 günlük takvim verisi oluştur
   * Her gün için entry varsa duygu durumunu ekle
   */
  const getLast7Days = () => {
    const days = [];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      date.setHours(0, 0, 0, 0);
      
      const entry = entries.find(e => {
        const entryDate = new Date(e.created_at);
        entryDate.setHours(0, 0, 0, 0);
        return entryDate.getTime() === date.getTime();
      });
      
      days.push({
        date: date,
        dayName: ['Paz', 'Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt'][date.getDay()],
        dayNumber: date.getDate(),
        mood: entry ? entry.analiz_sonucu?.sentiment?.duygu : null,
        entry: entry
      });
    }
    
    return days;
  };

  /**
   * Mood'a göre emoji döndür
   */
  const getMoodEmoji = (mood) => {
    if (!mood) return '⚪';
    if (mood === 'positive') return '😊';
    if (mood === 'negative') return '😔';
    return '😐';
  };

  /**
   * Mood'a göre border rengi
   */
  const getMoodColor = (mood) => {
    if (!mood) return COLORS.text_tertiary;
    if (mood === 'positive') return '#10B981';  // Yeşil
    if (mood === 'negative') return '#EF4444';  // Kırmızı
    return COLORS.warning;  // Turuncu (neutral)
  };

  /**
   * Hızlı istatistikler hesapla
   * - Ortalama pozitiflik yüzdesi
   * - En çok bahsedilen konu
   */
  const calculateQuickStats = () => {
    if (entries.length === 0) return null;
    
    const positiveCount = entries.filter(e => e.analiz_sonucu?.sentiment?.duygu === 'positive').length;
    const avgMood = (positiveCount / entries.length * 100).toFixed(0);
    
    const topicCounts = {};
    entries.forEach(e => {
      const topics = e.analiz_sonucu?.topics || [];
      topics.forEach(t => {
        topicCounts[t] = (topicCounts[t] || 0) + 1;
      });
    });
    
    const sortedTopics = Object.entries(topicCounts).sort((a, b) => b[1] - a[1]);
    const topTopic = sortedTopics.length > 0 ? sortedTopics[0][0] : 'Henüz yok';
    
    return { avgMood, topTopic };
  };

  const motivationCard = getMotivationCard();
  const quickStats = calculateQuickStats();
  const last7Days = getLast7Days();

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        contentContainerStyle={{ paddingBottom: 100 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadData} tintColor={COLORS.accent} />}
      >
        {/* Header */}
        <View style={styles.header}>
            <Text style={styles.greeting}>Hoş geldin!</Text>
            <Text style={styles.subGreeting}>Bugün ruh halin nasıl?</Text>
        </View>
        
        {/* CTA Card */}
        <TouchableOpacity 
            style={styles.ctaCard}
            onPress={() => navigation.navigate('AddEntry')}
        >
          <Text style={styles.ctaTitle}>Günlüğüne Yaz</Text>
          <Text style={styles.ctaSubtitle}>Bugün neler yaşadın, anlatmak ister misin?</Text>
          <View style={styles.ctaIcon}>
            <Ionicons name="arrow-forward" size={24} color="#FFF" />
          </View>
        </TouchableOpacity>

        {/* 🆕 AKILLI MOTİVASYON KARTI */}
        <View style={styles.section}>
          <View style={[styles.motivationCard, { borderLeftColor: motivationCard.borderColor }]}>
            <View style={styles.motivationHeader}>
              <Ionicons name={motivationCard.icon} size={28} color={motivationCard.iconColor} />
              <Text style={styles.motivationTitle}>{motivationCard.title}</Text>
            </View>
            <Text style={styles.motivationText}>{motivationCard.message}</Text>
            
            {motivationCard.showButton && (
              <TouchableOpacity 
                style={styles.viewEntryButton}
                onPress={motivationCard.buttonAction}
              >
                <Text style={styles.viewEntryButtonText}>{motivationCard.buttonText}</Text>
                <Ionicons name="arrow-forward" size={16} color={COLORS.primary} />
              </TouchableOpacity>
            )}

            {motivationCard.quote && (
              <Text style={styles.motivationQuote}>💭 {motivationCard.quote}</Text>
            )}
          </View>
        </View>
        
        {/* HAFTALIK MOOD TAKVİMİ */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Haftalık Ruh Halin</Text>
          <View style={styles.calendarContainer}>
            {last7Days.map((day, index) => (
              <TouchableOpacity 
                key={index} 
                style={[
                  styles.dayCard,
                  day.mood && { 
                    borderColor: getMoodColor(day.mood), 
                    borderWidth: 2,
                    backgroundColor: day.mood ? `${getMoodColor(day.mood)}15` : COLORS.card_elevated
                  }
                ]}
                onPress={() => {
                  if (day.entry) {
                    navigation.navigate('Entries');  // ✅ DÜZELTİLDİ: 'Journal' → 'Entries'
                  }
                }}
                activeOpacity={day.entry ? 0.7 : 1}
              >
                <Text style={styles.dayName}>{day.dayName}</Text>
                <Text style={styles.dayEmoji}>{getMoodEmoji(day.mood)}</Text>
                <Text style={styles.dayNumber}>{day.dayNumber}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <Text style={styles.calendarHint}>
            💡 Renkli günlere tıklayarak detayları görüntüle
          </Text>
        </View>

        {/* HIZLI İSTATİSTİKLER */}
        {quickStats && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Bu Ay</Text>
            <View style={styles.quickStatsContainer}>
              <View style={styles.quickStatCard}>
                <Ionicons name="analytics" size={32} color={COLORS.accent} />
                <Text style={styles.quickStatLabel}>Pozitiflik Oranı</Text>
                <Text style={styles.quickStatValue}>{quickStats.avgMood}%</Text>
              </View>
              <View style={styles.quickStatCard}>
                <Ionicons name="bookmark" size={32} color={COLORS.primary} />
                <Text style={styles.quickStatLabel}>En Çok Yazdığın</Text>
                <Text style={styles.quickStatValue} numberOfLines={1}>
                  {quickStats.topTopic}
                </Text>
              </View>
            </View>
          </View>
        )}

        {/* Seri + Toplam İstatistikleri */}
        <View style={styles.statsContainer}>
          <View style={[styles.statCard, {marginRight: 16}]}>
            <Ionicons name="flame" size={28} color={COLORS.warning} />
            <Text style={styles.statLabel}>Seri</Text>
            <Text style={styles.statValue}>{stats.streak} Gün</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="journal" size={28} color={COLORS.accent} />
            <Text style={styles.statLabel}>Toplam</Text>
            <Text style={styles.statValue}>{stats.total}</Text>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: { padding: 20 },
  greeting: { fontSize: 32, fontWeight: 'bold', color: COLORS.text_primary },
  subGreeting: { fontSize: 16, color: COLORS.text_secondary, marginTop: 5 },
  
  ctaCard: {
    backgroundColor: COLORS.card,
    margin: 20,
    marginTop: 0,
    padding: 24,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: COLORS.card_elevated,
    position: 'relative',
  },
  ctaTitle: { fontSize: 22, fontWeight: 'bold', color: COLORS.text_primary, marginBottom: 8 },
  ctaSubtitle: { fontSize: 14, color: COLORS.text_secondary, maxWidth: '80%' },
  ctaIcon: { 
    position: 'absolute', right: 20, top: 35, 
    backgroundColor: COLORS.primary, padding: 12, borderRadius: 50 
  },

  section: { paddingHorizontal: 20, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text_primary, marginBottom: 12 },

  // Haftalık Takvim
  calendarContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: COLORS.card,
    padding: 12,
    borderRadius: 16,
  },
  dayCard: {
    flex: 1,
    alignItems: 'center',
    padding: 8,
    marginHorizontal: 2,
    borderRadius: 12,
    backgroundColor: COLORS.card_elevated,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  dayName: { 
    fontSize: 10, 
    color: COLORS.text_tertiary, 
    marginBottom: 4, 
    fontWeight: '600' 
  },
  dayEmoji: { fontSize: 24, marginVertical: 4 },
  dayNumber: { 
    fontSize: 12, 
    color: COLORS.text_secondary, 
    marginTop: 4 
  },
  calendarHint: { 
    fontSize: 11, 
    color: COLORS.text_tertiary, 
    textAlign: 'center', 
    marginTop: 8,
    fontStyle: 'italic'
  },

  // Hızlı İstatistikler
  quickStatsContainer: { flexDirection: 'row', gap: 12 },
  quickStatCard: {
    flex: 1,
    backgroundColor: COLORS.card,
    padding: 16,
    borderRadius: 16,
    alignItems: 'center',
  },
  quickStatLabel: { 
    fontSize: 11, 
    color: COLORS.text_tertiary, 
    textAlign: 'center', 
    marginTop: 8,
    marginBottom: 4
  },
  quickStatValue: { 
    fontSize: 18, 
    fontWeight: 'bold', 
    color: COLORS.text_primary, 
    textAlign: 'center' 
  },

  statsContainer: { flexDirection: 'row', paddingHorizontal: 20 },
  statCard: { 
    flex: 1, 
    backgroundColor: COLORS.card_elevated, 
    borderRadius: 20, 
    padding: 20, 
    alignItems: 'center' 
  },
  statLabel: { color: COLORS.text_secondary, fontSize: 14, marginTop: 8 },
  statValue: { color: COLORS.text_primary, fontSize: 24, fontWeight: 'bold', marginTop: 4 },

  // 🆕 Motivasyon Kartı
  motivationCard: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  motivationHeader: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    gap: 10, 
    marginBottom: 12 
  },
  motivationTitle: { 
    color: COLORS.text_primary, 
    fontWeight: 'bold', 
    fontSize: 18,
    flex: 1
  },
  motivationText: { 
    color: COLORS.text_secondary, 
    fontSize: 14, 
    lineHeight: 22,
    marginBottom: 4
  },
  motivationQuote: {
    color: COLORS.text_tertiary,
    fontSize: 13,
    fontStyle: 'italic',
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: COLORS.card_elevated
  },
  viewEntryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginTop: 12,
    paddingVertical: 10,
    paddingHorizontal: 16,
    backgroundColor: COLORS.card_elevated,
    borderRadius: 12,
    alignSelf: 'flex-start'
  },
  viewEntryButtonText: {
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600'
  },
});