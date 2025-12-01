import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { LineChart } from "react-native-chart-kit";
import { Dimensions } from "react-native";
import { useFocusEffect } from '@react-navigation/native';
import { fetchEntries } from '../services/ApiService';

const screenWidth = Dimensions.get("window").width;

export default function HomeScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({ streak: 0, total: 0, lastMood: 0 });

  const loadData = async () => {
    setRefreshing(true);
    const data = await fetchEntries();
    setEntries(data);
    
    // Basit istatistik hesabı
    if (data.length > 0) {
        // Son duygu skorunu al (Simüle edilmiş user_mood yoksa analizden hesapla)
        // Burada basitlik için analizdeki duygu skorunu baz alıyoruz
        const lastEntry = data[0];
        const sentiment = lastEntry.analiz_sonucu?.sentiment?.skor || 0;
        setStats({
            streak: calculateStreak(data),
            total: data.length,
            lastMood: sentiment
        });
    }
    setRefreshing(false);
  };

  // Ekran her odaklandığında veriyi yenile
  useFocusEffect(
    useCallback(() => {
      loadData();
    }, [])
  );

  // Basit streak hesaplama (ardışık günler)
  const calculateStreak = (data) => {
      // Gerçek mantık burada olacak, şimdilik dummy
      return data.length > 0 ? Math.min(data.length, 5) : 0; 
  };

  // Grafik verisini hazırla (Son 7 kayıt)
  const chartData = {
    labels: entries.slice(0, 7).reverse().map(e => {
        const date = new Date(e.created_at);
        return `${date.getDate()}/${date.getMonth()+1}`;
    }),
    datasets: [
      {
        data: entries.slice(0, 7).reverse().map(e => {
            // Duygu skorunu (-1 ile 1 arası) grafiğe döküyoruz
            let score = e.analiz_sonucu?.sentiment?.skor || 0;
            if (e.analiz_sonucu?.sentiment?.duygu === 'negative') score *= -1;
            return score;
        }),
        color: (opacity = 1) => `rgba(255, 193, 7, ${opacity})`, // Accent color
        strokeWidth: 2
      }
    ],
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        contentContainerStyle={{ paddingBottom: 100 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadData} tintColor={COLORS.accent} />}
      >
        <View style={styles.header}>
            <Text style={styles.greeting}>Hoş geldin!</Text>
            <Text style={styles.subGreeting}>Bugün ruh halin nasıl?</Text>
        </View>
        
        {/* Büyük CTA Kartı */}
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
        
        {/* Grafik Alanı */}
        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Duygu Trendi</Text>
            {entries.length > 0 ? (
                <LineChart
                    data={chartData}
                    width={screenWidth - 40}
                    height={220}
                    chartConfig={{
                    backgroundColor: COLORS.card,
                    backgroundGradientFrom: COLORS.card,
                    backgroundGradientTo: COLORS.card,
                    decimalPlaces: 1,
                    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
                    labelColor: (opacity = 1) => `rgba(148, 163, 184, ${opacity})`,
                    style: { borderRadius: 16 },
                    propsForDots: {
                        r: "6",
                        strokeWidth: "2",
                        stroke: COLORS.accent
                    }
                    }}
                    bezier
                    style={{ marginVertical: 8, borderRadius: 16 }}
                />
            ) : (
                <View style={styles.emptyChart}>
                    <Text style={{color: COLORS.text_secondary}}>Veri bekleniyor...</Text>
                </View>
            )}
        </View>

        {/* İstatistikler */}
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
    overflow: 'hidden'
  },
  ctaTitle: { fontSize: 22, fontWeight: 'bold', color: COLORS.text_primary, marginBottom: 8 },
  ctaSubtitle: { fontSize: 14, color: COLORS.text_secondary, maxWidth: '80%' },
  ctaIcon: { 
    position: 'absolute', right: 20, top: 35, 
    backgroundColor: COLORS.primary, padding: 12, borderRadius: 50 
  },

  section: { paddingHorizontal: 20, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text_primary, marginBottom: 12 },
  emptyChart: { height: 220, backgroundColor: COLORS.card, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },

  statsContainer: { flexDirection: 'row', paddingHorizontal: 20 },
  statCard: { flex: 1, backgroundColor: COLORS.card_elevated, borderRadius: 20, padding: 20, alignItems: 'center' },
  statLabel: { color: COLORS.text_secondary, fontSize: 14, marginTop: 8 },
  statValue: { color: COLORS.text_primary, fontSize: 24, fontWeight: 'bold', marginTop: 4 },
});