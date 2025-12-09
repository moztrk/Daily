import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { PieChart } from "react-native-chart-kit";
import { fetchEntries, fetchDailyInsight } from '../services/ApiService';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

const screenWidth = Dimensions.get("window").width;

export default function ReportsScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  // Varsayılan bir değer atadık ki ekran boş kalmasın
  const [insightData, setInsightData] = useState({ insight: "Veriler analiz ediliyor...", trend: "neutral" });
  const [relatedEntries, setRelatedEntries] = useState([]); 
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    positive: 0, negative: 0, neutral: 0,
    topTopic: 'Yok'
  });

  const loadData = async () => {
    setRefreshing(true);
    try {
        const [data, insight] = await Promise.all([
            fetchEntries(),
            fetchDailyInsight()
        ]);
        
        setEntries(data);
        
        // Gelen veriyi kontrol et, boşsa varsayılanı koru
        if (insight && insight.insight) {
            setInsightData(insight);
        }
        
        calculateStats(data);

        // İlgili günlükleri bulma mantığı
        if (insight && insight.related_topic) {
            const topic = insight.related_topic;
            const filtered = data.filter(e => 
                e.analiz_sonucu?.topics?.includes(topic)
            ).slice(0, 5); // Son 5 tanesi
            setRelatedEntries(filtered);
        } else {
            setRelatedEntries([]);
        }

    } catch (e) {
        console.log("Veri yükleme hatası:", e);
    } finally {
        setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadData();
    }, [])
  );

  const calculateStats = (data) => {
    let pos = 0, neg = 0, neu = 0;
    const topicCounts = {};
    
    data.forEach(entry => {
        const sentiment = entry.analiz_sonucu?.sentiment?.duygu;
        if (sentiment === 'positive') pos++;
        else if (sentiment === 'negative') neg++;
        else neu++;

        const topics = entry.analiz_sonucu?.topics || [];
        topics.forEach(t => {
            topicCounts[t] = (topicCounts[t] || 0) + 1;
        });
    });

    let maxTopic = 'Yok';
    let maxCount = 0;
    for (const [topic, count] of Object.entries(topicCounts)) {
        if (count > maxCount) {
            maxCount = count;
            maxTopic = topic;
        }
    }
    setStats({ positive: pos, negative: neg, neutral: neu, topTopic: maxTopic });
  };

  const pieData = [
    { name: "Pozitif", population: stats.positive, color: COLORS.positive, legendFontColor: "#ccc", legendFontSize: 12 },
    { name: "Negatif", population: stats.negative, color: COLORS.negative, legendFontColor: "#ccc", legendFontSize: 12 },
    { name: "Nötr", population: stats.neutral, color: COLORS.text_tertiary, legendFontColor: "#ccc", legendFontSize: 12 }
  ];

  // Trend rengini belirle
  const getTrendColor = (trend) => {
      if (trend === 'positive') return COLORS.positive;
      if (trend === 'negative') return COLORS.negative;
      return COLORS.warning; // Varsayılan Sarı
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.headerTitle}>Analiz Raporu</Text>
      
      <ScrollView 
        contentContainerStyle={{ padding: 20, paddingBottom: 100 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadData} tintColor={COLORS.accent} />}
      >
        
        {/* 1. YAPAY ZEKA İÇGÖRÜ KARTI */}
        <View style={[styles.tipCard, { 
            borderColor: getTrendColor(insightData?.trend),
            backgroundColor: COLORS.card 
        }]}>
            <View style={styles.tipHeader}>
                <Ionicons name="bulb" size={24} color={getTrendColor(insightData?.trend)} />
                <Text style={styles.tipTitle}>Yapay Zeka Analizi</Text>
            </View>
            <Text style={styles.tipText}>
                {insightData?.insight || "Verileriniz inceleniyor..."}
            </Text>
        </View>

        {/* 2. KANITLAR (İlgili Günlükler) */}
        {relatedEntries.length > 0 && (
            <View style={styles.evidenceSection}>
                <Text style={styles.evidenceTitle}>
                    Buna Sebep Olan Kayıtlar ({insightData?.related_topic})
                </Text>
                {relatedEntries.map(entry => (
                    <TouchableOpacity 
                        key={entry.id} 
                        style={styles.evidenceCard}
                        onPress={() => navigation.navigate('EntryDetail', { entry })} // Detaya git
                    >
                        <View style={styles.evidenceHeader}>
                            <Text style={styles.evidenceDate}>
                                {new Date(entry.created_at).toLocaleDateString('tr-TR')}
                            </Text>
                            <Ionicons 
                                name={entry.analiz_sonucu?.sentiment?.duygu === 'positive' ? 'happy' : 'sad'} 
                                size={16} 
                                color={entry.analiz_sonucu?.sentiment?.duygu === 'positive' ? COLORS.positive : COLORS.negative} 
                            />
                        </View>
                        <Text style={styles.evidenceText} numberOfLines={2}>
                            {entry.metin}
                        </Text>
                    </TouchableOpacity>
                ))}
            </View>
        )}

        {/* 3. PASTA GRAFİĞİ */}
        <View style={styles.chartCard}>
            <Text style={styles.cardTitle}>Genel Duygu Dağılımı</Text>
            {entries.length > 0 ? (
                <PieChart
                    data={pieData}
                    width={screenWidth - 60}
                    height={200}
                    chartConfig={{ color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})` }}
                    accessor={"population"}
                    backgroundColor={"transparent"}
                    paddingLeft={"15"}
                    center={[10, 0]}
                    absolute
                />
            ) : (
                <Text style={{color: COLORS.text_tertiary, textAlign: 'center', padding: 20}}>
                    Henüz veri yok. Günlük yazmaya başla!
                </Text>
            )}
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  headerTitle: { fontSize: 28, fontWeight: 'bold', color: COLORS.text_primary, padding: 20, paddingBottom: 0 },
  
  // Grafik Kartı
  chartCard: { backgroundColor: COLORS.card, borderRadius: 24, padding: 16, marginBottom: 20, marginTop: 20 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text_primary, marginBottom: 12 },

  // İpucu Kartı
  tipCard: { 
      borderRadius: 16, 
      padding: 16, 
      borderWidth: 1,
      marginBottom: 16,
      // Gölge efekti
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 4,
      elevation: 3,
  },
  tipHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 },
  tipTitle: { color: COLORS.text_primary, fontWeight: 'bold', fontSize: 16 },
  tipText: { color: "#E2E8F0", fontSize: 14, lineHeight: 22 }, // Rengi açtık, daha okunaklı olsun diye

  // Kanıt Listesi
  evidenceSection: { marginBottom: 10 },
  evidenceTitle: { color: COLORS.text_tertiary, fontSize: 12, textTransform: 'uppercase', marginBottom: 8, marginLeft: 4 },
  evidenceCard: { 
      backgroundColor: COLORS.card_elevated, 
      borderRadius: 12, 
      padding: 12, 
      marginBottom: 8,
      borderLeftWidth: 3,
      borderLeftColor: COLORS.text_tertiary
  },
  evidenceHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 },
  evidenceDate: { color: COLORS.text_tertiary, fontSize: 12, fontWeight: 'bold' },
  evidenceText: { color: COLORS.text_secondary, fontSize: 13 },
});