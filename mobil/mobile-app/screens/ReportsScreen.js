import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions, RefreshControl, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { PieChart } from "react-native-chart-kit";
import { fetchEntries, fetchDailyInsight } from '../services/ApiService';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient'; // Yeni eklenen paket

const screenWidth = Dimensions.get("window").width;

export default function ReportsScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  const [insightData, setInsightData] = useState({ insight: "Veriler analiz ediliyor...", trend: "neutral", source: "new_gen" });
  const [relatedEntries, setRelatedEntries] = useState([]); 
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    positive: 0, negative: 0, neutral: 0,
    topTopic: 'Belirsiz', totalCount: 0
  });

  const loadData = async () => {
    setRefreshing(true);
    try {
        const [data, insight] = await Promise.all([
            fetchEntries(),
            fetchDailyInsight()
        ]);
        
        setEntries(data);
        if (insight && insight.insight) setInsightData(insight);
        calculateStats(data);

        if (insight && insight.related_topic) {
            const topic = insight.related_topic;
            const filtered = data.filter(e => e.analiz_sonucu?.topics?.includes(topic)).slice(0, 5);
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
    useCallback(() => { loadData(); }, [])
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
        topics.forEach(t => { topicCounts[t] = (topicCounts[t] || 0) + 1; });
    });

    let maxTopic = 'Belirsiz';
    let maxCount = 0;
    for (const [topic, count] of Object.entries(topicCounts)) {
        if (count > maxCount) { maxCount = count; maxTopic = topic; }
    }
    setStats({ positive: pos, negative: neg, neutral: neu, topTopic: maxTopic, totalCount: data.length });
  };

  const pieData = [
    { name: "Mutlu", population: stats.positive, color: COLORS.positive, legendFontColor: COLORS.text_secondary, legendFontSize: 12 },
    { name: "Üzgün", population: stats.negative, color: COLORS.negative, legendFontColor: COLORS.text_secondary, legendFontSize: 12 },
    { name: "Nötr", population: stats.neutral, color: COLORS.text_tertiary, legendFontColor: COLORS.text_secondary, legendFontSize: 12 }
  ];

  const getTrendColor = (trend) => {
      if (trend === 'positive') return [COLORS.positive, '#10B981']; // Green gradient
      if (trend === 'negative') return [COLORS.negative, '#EF4444']; // Red gradient
      return [COLORS.accent, '#3B82F6']; // Blue gradient
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Analiz Merkezi</Text>
        <Text style={styles.headerSubtitle}>Ruh halinin dijital yansıması</Text>
      </View>
      
      <ScrollView 
        contentContainerStyle={{ padding: 20, paddingBottom: 100 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadData} tintColor={COLORS.accent} />}
        showsVerticalScrollIndicator={false}
      >
        
        {/* 1. YAPAY ZEKA İÇGÖRÜ KARTI (PREMIUM LOOK) */}
        <LinearGradient
            colors={['#2D3748', '#1A202C']}
            start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}
            style={[styles.aiCard, { borderColor: getTrendColor(insightData?.trend)[0] }]}
        >
            <View style={styles.aiHeader}>
                <View style={[styles.iconBox, { backgroundColor: getTrendColor(insightData?.trend)[0] + '20' }]}>
                    <Ionicons name="sparkles" size={20} color={getTrendColor(insightData?.trend)[0]} />
                </View>
                <Text style={styles.aiTitle}>AI Yaşam Koçu</Text>
                {insightData?.source === 'cache' && <Ionicons name="time-outline" size={14} color={COLORS.text_tertiary} style={{marginLeft: 'auto'}} />}
            </View>
            
            <Text style={styles.aiText}>
                {insightData?.insight}
            </Text>
        </LinearGradient>

        {/* 2. HIZLI İSTATİSTİKLER (GRID LAYOUT) */}
        <View style={styles.statsContainer}>
            <View style={styles.statBox}>
                <Text style={styles.statLabel}>Toplam Kayıt</Text>
                <Text style={styles.statValue}>{stats.totalCount}</Text>
                <Ionicons name="book-outline" size={18} color={COLORS.accent} style={styles.statIcon} />
            </View>
            <View style={styles.statBox}>
                <Text style={styles.statLabel}>Baskın Konu</Text>
                <Text style={styles.statValue} numberOfLines={1}>{stats.topTopic}</Text>
                <Ionicons name="chatbubble-ellipses-outline" size={18} color={COLORS.positive} style={styles.statIcon} />
            </View>
        </View>

        {/* 3. GRAFİK KARTI */}
        <View style={styles.chartCard}>
            <Text style={styles.sectionTitle}>Duygu Dağılımı</Text>
            {entries.length > 0 ? (
                <View style={{alignItems: 'center'}}>
                    <PieChart
                        data={pieData}
                        width={screenWidth - 40}
                        height={200}
                        chartConfig={{ color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})` }}
                        accessor={"population"}
                        backgroundColor={"transparent"}
                        paddingLeft={"15"}
                        center={[0, 0]}
                        absolute
                        hasLegend={true}
                    />
                </View>
            ) : (
                <Text style={styles.emptyText}>Henüz yeterli veri yok.</Text>
            )}
        </View>

        {/* 4. KANITLAR (İLİŞKİLİ KAYITLAR) */}
        {relatedEntries.length > 0 && (
            <View style={styles.evidenceSection}>
                <Text style={styles.sectionTitle}>
                    🔍 Analize Kaynaklık Edenler
                </Text>
                {relatedEntries.map((entry, index) => (
                    <TouchableOpacity 
                        key={entry.id} 
                        style={styles.evidenceCard}
                        onPress={() => navigation.navigate('EntryDetail', { entry })}
                        activeOpacity={0.7}
                    >
                        <LinearGradient
                             colors={[COLORS.card, COLORS.card_elevated]}
                             style={styles.evidenceGradient}
                        >
                            <View style={styles.evidenceRow}>
                                <View style={[styles.moodDot, { 
                                    backgroundColor: entry.analiz_sonucu?.sentiment?.duygu === 'positive' ? COLORS.positive : 
                                                    entry.analiz_sonucu?.sentiment?.duygu === 'negative' ? COLORS.negative : COLORS.warning 
                                }]} />
                                <Text style={styles.evidenceDate}>
                                    {new Date(entry.created_at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })}
                                </Text>
                            </View>
                            <Text style={styles.evidenceText} numberOfLines={2}>
                                {entry.metin}
                            </Text>
                            <Ionicons name="chevron-forward" size={16} color={COLORS.text_tertiary} style={styles.chevron} />
                        </LinearGradient>
                    </TouchableOpacity>
                ))}
            </View>
        )}

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: { paddingHorizontal: 20, paddingTop: 10, paddingBottom: 5 },
  headerTitle: { fontSize: 32, fontWeight: '800', color: COLORS.text_primary },
  headerSubtitle: { fontSize: 14, color: COLORS.text_tertiary, marginTop: -5 },

  // AI Card Styles
  aiCard: {
      borderRadius: 20,
      padding: 20,
      marginBottom: 24,
      borderWidth: 1,
      elevation: 5,
      shadowColor: COLORS.accent,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: 8,
  },
  aiHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  iconBox: { padding: 8, borderRadius: 12, marginRight: 10 },
  aiTitle: { fontSize: 18, fontWeight: '700', color: COLORS.text_primary },
  aiText: { fontSize: 15, lineHeight: 24, color: COLORS.text_secondary, fontWeight: '500' },

  // Stats Grid
  statsContainer: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 24, gap: 12 },
  statBox: { 
      flex: 1, 
      backgroundColor: COLORS.card, 
      borderRadius: 16, 
      padding: 16, 
      position: 'relative',
      borderWidth: 1,
      borderColor: COLORS.border || '#333'
  },
  statLabel: { fontSize: 12, color: COLORS.text_tertiary, marginBottom: 4, textTransform: 'uppercase', letterSpacing: 0.5 },
  statValue: { fontSize: 20, fontWeight: 'bold', color: COLORS.text_primary },
  statIcon: { position: 'absolute', right: 12, top: 12, opacity: 0.8 },

  // Chart & Section Styles
  chartCard: { backgroundColor: COLORS.card, borderRadius: 24, padding: 20, marginBottom: 24 },
  sectionTitle: { fontSize: 18, fontWeight: '700', color: COLORS.text_primary, marginBottom: 16 },
  emptyText: { color: COLORS.text_tertiary, textAlign: 'center', padding: 20 },

  // Evidence List Styles
  evidenceSection: { marginBottom: 20 },
  evidenceCard: { marginBottom: 12, borderRadius: 16, overflow: 'hidden' },
  evidenceGradient: { padding: 16 },
  evidenceRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  moodDot: { width: 8, height: 8, borderRadius: 4, marginRight: 8 },
  evidenceDate: { fontSize: 12, color: COLORS.text_tertiary, fontWeight: '600' },
  evidenceText: { fontSize: 14, color: COLORS.text_secondary, lineHeight: 20, paddingRight: 20 },
  chevron: { position: 'absolute', right: 16, top: '50%', marginTop: -8 },
});