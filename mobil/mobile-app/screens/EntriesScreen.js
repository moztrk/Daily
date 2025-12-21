/**
 * EntriesScreen - Premium Timeline Tasarımı
 * 
 * Özellikler:
 * ✅ Zaman Tüneli (Timeline) - Hikaye formatı
 * ✅ Arama Çubuğu - Anlık filtreleme
 * ✅ Kategori Filtreleri (Chips) - Hızlı erişim
 * ✅ Gradient Kartlar - Modern görünüm
 * ✅ 5 Seviyeli Mood Sistemi
 */

import React, { useState, useCallback, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, TextInput, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
import { fetchEntries } from '../services/ApiService';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

export default function EntriesScreen({ navigation }) {
  const [entries, setEntries] = useState([]);
  const [filteredEntries, setFilteredEntries] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState('Tümü');

  useFocusEffect(
    useCallback(() => {
      fetchEntries().then(data => {
        setEntries(data);
        setFilteredEntries(data);
      });
    }, [])
  );

  /**
   * Arama ve Filtreleme Mantığı
   * Her değişiklikte otomatik çalışır
   */
  useEffect(() => {
    let result = entries;

    // 1. Arama Filtresi (metin ve konularda)
    if (searchQuery) {
        result = result.filter(e => 
            e.metin.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (e.analiz_sonucu?.topics || []).some(t => t.toLowerCase().includes(searchQuery.toLowerCase()))
        );
    }

    // 2. Mood Filtresi
    if (activeFilter !== 'Tümü') {
        if (activeFilter === 'Mutlu') {
            result = result.filter(e => e.analiz_sonucu?.sentiment?.duygu === 'positive');
        } else if (activeFilter === 'Üzgün') {
            result = result.filter(e => e.analiz_sonucu?.sentiment?.duygu === 'negative');
        } else if (activeFilter === 'Nötr') {
            result = result.filter(e => e.analiz_sonucu?.sentiment?.duygu === 'neutral' || !e.analiz_sonucu?.sentiment);
        }
    }

    setFilteredEntries(result);
  }, [searchQuery, activeFilter, entries]);

  /**
   * 5 Seviyeli Sentiment İkonu
   */
  const getSentimentIcon = (sentiment) => {
    if (!sentiment) return { icon: 'happy-outline', color: COLORS.text_tertiary };
    
    const { duygu, skor = 0.5 } = sentiment;

    if (duygu === 'positive') {
      return skor >= 0.7 
        ? { icon: 'happy', color: '#10B981' } 
        : { icon: 'happy-outline', color: '#34D399' };
    }
    
    if (duygu === 'negative') {
      return skor >= 0.7 
        ? { icon: 'sad', color: '#EF4444' } 
        : { icon: 'sad-outline', color: '#F87171' };
    }
    
    return { icon: 'happy-outline', color: '#F59E0B' }; // Neutral
  };

  /**
   * Filtre Chip Render
   */
  const renderFilterChip = (label, icon) => (
      <TouchableOpacity 
        style={[styles.filterChip, activeFilter === label && styles.activeChip]}
        onPress={() => setActiveFilter(label)}
      >
          {icon && <Ionicons name={icon} size={14} color={activeFilter === label ? '#FFF' : COLORS.text_tertiary} style={{marginRight: 4}} />}
          <Text style={[styles.filterText, activeFilter === label && styles.activeFilterText]}>{label}</Text>
      </TouchableOpacity>
  );

  /**
   * Timeline Item Render
   */
  const renderItem = ({ item, index }) => {
    const date = new Date(item.created_at);
    const day = date.getDate();
    const month = date.toLocaleDateString('tr-TR', { month: 'short' });
    const timeStr = date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    
    const sentimentData = item.analiz_sonucu?.sentiment;
    const { icon, color } = getSentimentIcon(sentimentData);
    const topics = item.analiz_sonucu?.topics || [];
    const isLast = index === filteredEntries.length - 1;

    return (
      <View style={styles.timelineRow}>
        {/* SOL: Tarih ve Dikey Çizgi */}
        <View style={styles.timelineLeft}>
            <View style={styles.dateBadge}>
                <Text style={styles.dateDay}>{day}</Text>
                <Text style={styles.dateMonth}>{month}</Text>
            </View>
            {!isLast && <View style={styles.timelineLine} />}
        </View>

        {/* ORTA: Mood İkonu */}
        <View style={styles.timelineNode}>
             <View style={[styles.iconCircle, { borderColor: color }]}>
                 <Ionicons name={icon} size={16} color={color} />
             </View>
        </View>

        {/* SAĞ: Günlük Kartı */}
        <TouchableOpacity 
            style={styles.timelineContent}
            onPress={() => navigation.navigate('EntryDetail', { entry: item })}
            activeOpacity={0.8}
        >
            <LinearGradient
                colors={[COLORS.card, COLORS.card_elevated]}
                style={styles.cardGradient}
            >
                <View style={styles.cardHeader}>
                    <Text style={styles.time}>{timeStr}</Text>
                    {topics.length > 0 && <Text style={styles.topicLabel}>{topics[0]}</Text>}
                </View>
                
                <Text style={styles.previewText} numberOfLines={3}>{item.metin}</Text>
                
                <View style={styles.cardFooter}>
                    <Ionicons name="chevron-forward" size={16} color={COLORS.accent} />
                </View>
            </LinearGradient>
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* HEADER: Başlık ve Arama */}
      <View style={styles.header}>
          <Text style={styles.headerTitle}>Günlüklerim</Text>
          <View style={styles.searchContainer}>
              <Ionicons name="search" size={20} color={COLORS.text_tertiary} style={styles.searchIcon} />
              <TextInput 
                  style={styles.searchInput}
                  placeholder="Anılarını ara..."
                  placeholderTextColor={COLORS.text_tertiary}
                  value={searchQuery}
                  onChangeText={setSearchQuery}
              />
              {searchQuery.length > 0 && (
                  <TouchableOpacity onPress={() => setSearchQuery('')}>
                      <Ionicons name="close-circle" size={20} color={COLORS.text_tertiary} />
                  </TouchableOpacity>
              )}
          </View>
      </View>

      {/* FILTRELER (Horizontal Scroll) */}
      <View style={styles.filterContainer}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{paddingHorizontal: 20}}>
              {renderFilterChip('Tümü', 'grid')}
              {renderFilterChip('Mutlu', 'happy')}
              {renderFilterChip('Nötr', 'remove-circle')}
              {renderFilterChip('Üzgün', 'sad')}
          </ScrollView>
      </View>

      {/* TIMELINE LİSTESİ */}
      <FlatList
        data={filteredEntries}
        renderItem={renderItem}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={{ padding: 20, paddingBottom: 100 }}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
            <View style={styles.emptyContainer}>
                <Ionicons name="journal-outline" size={48} color={COLORS.text_tertiary} />
                <Text style={styles.emptyText}>Kayıt bulunamadı.</Text>
            </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  
  // Header & Search
  header: { padding: 20, paddingBottom: 10 },
  headerTitle: { fontSize: 28, fontWeight: '800', color: COLORS.text_primary, marginBottom: 16 },
  searchContainer: { 
      flexDirection: 'row', 
      alignItems: 'center', 
      backgroundColor: COLORS.card, 
      borderRadius: 12, 
      paddingHorizontal: 12,
      height: 48,
      borderWidth: 1,
      borderColor: COLORS.card_elevated
  },
  searchIcon: { marginRight: 8 },
  searchInput: { flex: 1, color: COLORS.text_primary, fontSize: 16 },

  // Filters - Daha oval ve küçük
  filterContainer: { height: 44, marginBottom: 10 },
  filterChip: { 
      flexDirection: 'row', 
      alignItems: 'center', 
      backgroundColor: COLORS.card, 
      paddingHorizontal: 12,  // 16'dan 12'ye düşürüldü
      paddingVertical: 6,     // 8'den 6'ya düşürüldü
      borderRadius: 18,       // 20'den 18'e (daha oval)
      marginRight: 6,         // 8'den 6'ya
      borderWidth: 1,
      borderColor: COLORS.card_elevated
  },
  activeChip: { 
      backgroundColor: COLORS.accent, 
      borderColor: COLORS.accent 
  },
  filterText: { 
      color: COLORS.text_tertiary, 
      fontSize: 12,           // 13'ten 12'ye
      fontWeight: '600' 
  },
  activeFilterText: { color: '#FFF' },

  // Timeline Layout
  timelineRow: { flexDirection: 'row', marginBottom: 20 },
  timelineLeft: { alignItems: 'center', width: 40, marginRight: 10 },
  dateBadge: { alignItems: 'center', marginBottom: 4 },
  dateDay: { fontSize: 18, fontWeight: 'bold', color: COLORS.text_primary },
  dateMonth: { fontSize: 10, color: COLORS.text_tertiary, textTransform: 'uppercase' },
  timelineLine: { flex: 1, width: 2, backgroundColor: COLORS.card_elevated, marginTop: 4 },
  
  timelineNode: { width: 20, alignItems: 'center', marginTop: 12, marginRight: 10, zIndex: 2 },
  iconCircle: { 
      width: 24, height: 24, borderRadius: 12, 
      backgroundColor: COLORS.background, 
      borderWidth: 2, 
      justifyContent: 'center', alignItems: 'center' 
  },

  timelineContent: { flex: 1 },
  cardGradient: { 
      borderRadius: 16, 
      padding: 16, 
      borderWidth: 1, 
      borderColor: 'rgba(255,255,255,0.05)' 
  },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  time: { color: COLORS.text_tertiary, fontSize: 12, fontWeight: '600' },
  topicLabel: { 
      fontSize: 10, color: COLORS.accent, backgroundColor: 'rgba(59, 130, 246, 0.1)', 
      paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4, overflow: 'hidden' 
  },
  previewText: { color: COLORS.text_secondary, fontSize: 14, lineHeight: 20, marginBottom: 8 },
  cardFooter: { alignItems: 'flex-end' },

  // Empty State
  emptyContainer: { alignItems: 'center', marginTop: 60, opacity: 0.5 },
  emptyText: { color: COLORS.text_tertiary, marginTop: 10 },
});