import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { Ionicons } from '@expo/vector-icons';

export default function EntryDetailScreen({ route, navigation }) {
  const { entry } = route.params;
  const analysis = entry.analiz_sonucu || {};
  const sentiment = analysis.sentiment || {};
  
  const date = new Date(entry.created_at).toLocaleString('tr-TR');

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color={COLORS.text_primary} />
        </TouchableOpacity>
        <Text style={styles.date}>{date}</Text>
      </View>

      <ScrollView contentContainerStyle={{ padding: 20 }}>
        {/* Metin Kartı */}
        <View style={styles.textCard}>
            <Text style={styles.entryText}>{entry.metin}</Text>
        </View>

        {/* AI Analiz Kartı */}
        <View style={styles.analysisCard}>
            <View style={styles.analysisHeader}>
                <Ionicons name="sparkles" size={20} color={COLORS.accent} />
                <Text style={styles.analysisTitle}>AI Analizi</Text>
            </View>
            
            <View style={styles.row}>
                <Text style={styles.label}>Duygu:</Text>
                <Text style={[styles.value, { 
                    color: sentiment.duygu === 'positive' ? COLORS.positive : 
                           sentiment.duygu === 'negative' ? COLORS.negative : COLORS.text_secondary 
                }]}>
                    {sentiment.duygu?.toUpperCase()} (%{Math.round(sentiment.skor * 100)})
                </Text>
            </View>

            <View style={styles.divider} />

            <Text style={styles.label}>Konular:</Text>
            <View style={styles.tagContainer}>
                {analysis.topics?.map((t, i) => (
                    <View key={i} style={styles.tag}>
                        <Text style={styles.tagText}>{t}</Text>
                    </View>
                ))}
            </View>

            <View style={styles.divider} />

            <Text style={styles.label}>Tespit Edilen Varlıklar:</Text>
            {analysis.entities?.length > 0 ? (
                analysis.entities.map((e, i) => (
                    <Text key={i} style={styles.entityText}>
                        • <Text style={{fontWeight:'bold'}}>{e.metin}</Text> ({e.varlik})
                    </Text>
                ))
            ) : (
                <Text style={styles.entityText}>Özel bir varlık tespit edilemedi.</Text>
            )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: { flexDirection: 'row', alignItems: 'center', padding: 16, borderBottomWidth: 1, borderBottomColor: COLORS.card_elevated },
  backButton: { padding: 8, marginRight: 16 },
  date: { color: COLORS.text_secondary, fontSize: 16 },
  
  textCard: { backgroundColor: COLORS.card, padding: 20, borderRadius: 16, marginBottom: 20 },
  entryText: { color: COLORS.text_primary, fontSize: 16, lineHeight: 24 },
  
  analysisCard: { backgroundColor: COLORS.card_elevated, padding: 20, borderRadius: 16, borderColor: COLORS.primary, borderWidth: 1 },
  analysisHeader: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  analysisTitle: { color: COLORS.accent, fontWeight: 'bold', fontSize: 16 },
  
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  label: { color: COLORS.text_tertiary, fontSize: 14, marginBottom: 8 },
  value: { fontWeight: 'bold', fontSize: 16 },
  
  divider: { height: 1, backgroundColor: COLORS.card, marginVertical: 12 },
  
  tagContainer: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tag: { backgroundColor: COLORS.primary, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8 },
  tagText: { color: '#FFF', fontSize: 12 },
  
  entityText: { color: COLORS.text_secondary, fontSize: 14, marginTop: 4 },
});