import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';
import { LineChart } from "react-native-chart-kit";
import { Dimensions } from "react-native";
import { useFocusEffect } from '@react-navigation/native';
// Tek satırda temiz import
import { fetchEntries, fetchDailyInsight } from '../services/ApiService';

const screenWidth = Dimensions.get("window").width;

export default function HomeScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({ streak: 0, total: 0, lastMood: 0 });
  const [insight, setInsight] = useState("Verileriniz analiz ediliyor...");

  const loadData = async () => {
    setRefreshing(true);

    try {
        // Paralel olarak verileri ve içgörüyü çek
        const [data, insightResult] = await Promise.all([
            fetchEntries(),
            fetchDailyInsight()
        ]);

        setEntries(data);
        
        // --- DÜZELTME BURADA ---
        // Gelen 'insightResult' bir obje olduğu için içindeki .insight metnini alıyoruz.
        // Eğer obje değilse veya boşsa varsayılanı koruyoruz.
        if (insightResult && typeof insightResult === 'object' && insightResult.insight) {
            setInsight(insightResult.insight);
        } else if (typeof insightResult === 'string') {
            setInsight(insightResult);
        }
        // -----------------------
        
        // İstatistik hesabı
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

  const calculateStreak = (data) => {
      return data.length > 0 ? Math.min(data.length, 5) : 0; 
  };

  const chartData = {
    labels: entries.slice(0, 7).reverse().map(e => {
        const date = new Date(e.created_at);
        return `${date.getDate()}/${date.getMonth()+1}`;
    }),
    datasets: [
      {
        data: entries.slice(0, 7).reverse().map(e => {
            let score = e.analiz_sonucu?.sentiment?.skor || 0;
            if (e.analiz_sonucu?.sentiment?.duygu === 'negative') score *= -1;
            return score;
        }),
        color: (opacity = 1) => `rgba(255, 193, 7, ${opacity})`,
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
        
        {/* 1. Büyük CTA Kartı (Yazma Butonu) */}
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

        {/* 2. Yapay Zeka İçgörüsü */}
        <View style={styles.section}>
            <View style={styles.insightCard}>
                <View style={styles.insightHeader}>
                    <Ionicons name="sparkles" size={20} color={COLORS.accent} />
                    <Text style={styles.insightTitle}>Yapay Zeka İçgörüsü</Text>
                </View>
                {/* Burada artık kesinlikle bir String render ediliyor */}
                <Text style={styles.insightText}>
                    "{insight}"
                </Text>
            </View>
        </View>
        
        {/* 3. Grafik Alanı */}
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

        {/* 4. İstatistikler */}
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

  insightCard: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 0, 
    borderLeftWidth: 4,
    borderLeftColor: COLORS.accent,
    shadowColor: COLORS.accent,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 2,
  },
  insightHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  insightTitle: { color: COLORS.text_primary, fontWeight: 'bold', fontSize: 16 },
  insightText: { color: COLORS.text_secondary, fontSize: 14, lineHeight: 22, fontStyle: 'italic' },
});