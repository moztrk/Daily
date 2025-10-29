// screens/EntriesScreen.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS } from '../constants/colors';
export default function EntriesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.text}>Entries Screen (Takvim/Arşiv)</Text>
    </SafeAreaView>
  );
}
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background, justifyContent: 'center', alignItems: 'center' },
  text: { color: COLORS.text_primary, fontSize: 20 }
});