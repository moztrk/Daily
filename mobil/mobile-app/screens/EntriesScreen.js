import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { fetchEntries } from '../services/ApiService';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

export default function EntriesScreen({ navigation }) {
  const [entries, setEntries] = useState([]);

  useFocusEffect(
    useCallback(() => {
      fetchEntries().then(data => setEntries(data));
    }, [])
  );

  const getSentimentIcon = (sentiment) => {
      if (sentiment === 'positive') return { icon: 'happy', color: COLORS.positive };
      if (sentiment === 'negative') return { icon: 'sad', color: COLORS.negative };
      return { icon: 'remove', color: COLORS.text_tertiary }; // neutral
  };

  const renderItem = ({ item }) => {
    const date = new Date(item.created_at);
    const dateStr = date.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' });
    const timeStr = date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    
    const sentimentData = item.analiz_sonucu?.sentiment || { duygu: 'neutral' };
    const { icon, color } = getSentimentIcon(sentimentData.duygu);
    const topics = item.analiz_sonucu?.topics || [];

    return (
      <TouchableOpacity 
        style={styles.card}
        onPress={() => navigation.navigate('EntryDetail', { entry: item })}
      >
        <View style={styles.cardHeader}>
            <Text style={styles.date}>{dateStr}</Text>
            <Text style={styles.time}>{timeStr}</Text>
        </View>
        
        <Text style={styles.previewText} numberOfLines={2}>{item.metin}</Text>
        
        <View style={styles.cardFooter}>
            <View style={styles.tags}>
                {topics.slice(0, 2).map((t, i) => (
                    <View key={i} style={styles.tag}>
                        <Text style={styles.tagText}>{t}</Text>
                    </View>
                ))}
            </View>
            <Ionicons name={icon} size={24} color={color} />
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.headerTitle}>Günlüğüm</Text>
      <FlatList
        data={entries}
        renderItem={renderItem}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={{ padding: 20, paddingBottom: 100 }}
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  headerTitle: { fontSize: 28, fontWeight: 'bold', color: COLORS.text_primary, padding: 20, paddingBottom: 0 },
  
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary
  },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  date: { color: COLORS.text_primary, fontWeight: 'bold' },
  time: { color: COLORS.text_tertiary, fontSize: 12 },
  
  previewText: { color: COLORS.text_secondary, fontSize: 14, lineHeight: 20, marginBottom: 12 },
  
  cardFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  tags: { flexDirection: 'row', gap: 8 },
  tag: { backgroundColor: COLORS.card_elevated, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  tagText: { color: COLORS.text_secondary, fontSize: 10 },
});