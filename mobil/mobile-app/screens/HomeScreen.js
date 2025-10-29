// screens/HomeScreen.js
// (Ana sayfanın HTML'si çok karmaşık, şimdilik basit bir versiyonunu yapıyoruz)
import React from 'react';
import { View, Text, StyleSheet, StatusBar, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        <Text style={styles.title}>Welcome, Alex!</Text>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>How are you feeling today?</Text>
          <Text style={styles.cardSubtitle}>Write a few words...</Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Weekly Mood Trend</Text>
          <View style={styles.chartPlaceholder}>
             <Text style={styles.placeholderText}>[Duygu Grafiği Buraya Gelecek]</Text>
          </View>
        </View>

        <View style={styles.statsContainer}>
          <View style={[styles.statCard, {marginRight: 16}]}>
            <Ionicons name="flame" size={24} color={COLORS.warning} />
            <Text style={styles.statText}>Writing Streak</Text>
            <Text style={styles.statNumber}>12 Days</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="journal-outline" size={24} color={COLORS.accent} />
            <Text style={styles.statText}>Total Entries</Text>
            <Text style={styles.statNumber}>48</Text>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  title: { fontSize: 32, fontWeight: 'bold', color: COLORS.text_primary, paddingHorizontal: 20, marginVertical: 16 },
  card: { backgroundColor: COLORS.card, borderRadius: 16, padding: 20, marginHorizontal: 20, marginBottom: 16 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text_primary },
  cardSubtitle: { fontSize: 14, color: COLORS.text_secondary, marginTop: 4 },
  chartPlaceholder: { height: 120, justifyContent: 'center', alignItems: 'center', opacity: 0.5 },
  placeholderText: { color: COLORS.text_tertiary },
  statsContainer: { flexDirection: 'row', paddingHorizontal: 20 },
  statCard: { flex: 1, backgroundColor: COLORS.card_elevated, borderRadius: 16, padding: 20, alignItems: 'center' },
  statText: { color: COLORS.text_secondary, fontSize: 14, marginTop: 8 },
  statNumber: { color: COLORS.text_primary, fontSize: 24, fontWeight: 'bold', marginTop: 4 },
});