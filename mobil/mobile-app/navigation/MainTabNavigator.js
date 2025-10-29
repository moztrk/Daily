// navigation/MainTabNavigator.js
import React from 'react';
import { View, StyleSheet, Animated, Pressable, Easing, Dimensions } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS } from '../constants/colors';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// Ekranları import et
import HomeScreen from '../screens/HomeScreen';
import EntriesScreen from '../screens/EntriesScreen';
import AddEntryScreen from '../screens/AddEntryScreen';
import ReportsScreen from '../screens/ReportsScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const { width: SCREEN_W, height: SCREEN_H } = Dimensions.get('window');

// Animated LinearGradient component
const AnimatedLinearGradient = Animated.createAnimatedComponent(LinearGradient);

// Animated, gradient, expanding + button
const CustomTabBarButton = ({ children, onPress }) => {
  const scalePress = React.useRef(new Animated.Value(1)).current;
  const expand = React.useRef(new Animated.Value(0)).current;
  const opacity = React.useRef(new Animated.Value(0)).current;
  const isAnimatingRef = React.useRef(false);

  const onPressIn = () => {
    Animated.spring(scalePress, { toValue: 0.92, useNativeDriver: true }).start();
  };
  const onPressOut = () => {
    Animated.spring(scalePress, { toValue: 1, useNativeDriver: true }).start();
  };

  const handlePress = () => {
    if (isAnimatingRef.current) return;
    isAnimatingRef.current = true;

    opacity.setValue(1);
    expand.setValue(0);

    Animated.timing(expand, {
      toValue: 1,
      duration: 520,
      easing: Easing.out(Easing.poly(4)),
      useNativeDriver: true,
    }).start(() => {
      // --- DÜZELTME 2 ---
      // 'onPress' (navigasyon) animasyon BİTTİKTEN sonra tetiklenir
      try { onPress && onPress(); } catch (e) {} 
      
      // Animasyonu sıfırla (sayfa değişse bile)
      Animated.timing(opacity, { toValue: 0, duration: 200, delay: 100, useNativeDriver: true }).start(() => {
        expand.setValue(0);
        isAnimatingRef.current = false;
      });
    });
  };

  const circleSize = 76;
  const diagonal = Math.hypot(SCREEN_W, SCREEN_H);
  const maxScale = (diagonal / circleSize) * 1.1;

  const animatedScale = expand.interpolate({ inputRange: [0, 1], outputRange: [0.06, maxScale] });
  const animatedOpacity = opacity;

  return (
    <View style={{ flex: 1, alignItems: 'center' }}>
      
      <Animated.View
        pointerEvents="none"
        style={[
          StyleSheet.absoluteFill,
          { 
            alignItems: 'center', 
            justifyContent: 'center', 
            zIndex: 50, 
            opacity: animatedOpacity,
            top: -SCREEN_H / 2, 
          },
        ]}
      >
        <AnimatedLinearGradient
          colors={['#FFF176', '#FFD54F']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={{
            width: circleSize,
            height: circleSize,
            borderRadius: circleSize / 2,
            transform: [{ scale: animatedScale }],
          }}
        />
      </Animated.View>

      <Pressable
        onPress={handlePress}
        onPressIn={onPressIn}
        onPressOut={onPressOut}
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          top: -30, 
        }}
        accessibilityRole="button"
        accessibilityLabel="Add new entry"
      >
        <Animated.View
          style={[
            {
              width: 72,
              height: 72,
              borderRadius: 36,
              backgroundColor: '#FFD54F',
              justifyContent: 'center',
              alignItems: 'center',
            },
            styles.shadow,
            { transform: [{ scale: scalePress }] },
          ]}
        >
          <Ionicons name="add" color="#1f1f1f" size={36} /> 
        </Animated.View>
      </Pressable>
    </View>
  );
};

export default function MainTabNavigator() {
  const insets = useSafeAreaInsets();

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarShowLabel: false,
        tabBarActiveTintColor: COLORS.accent,
        tabBarInactiveTintColor: COLORS.text_tertiary,
        tabBarStyle: {
          backgroundColor: COLORS.card,
          borderTopColor: COLORS.card_elevated,
          position: 'absolute',
          elevation: 0,
          bottom: insets.bottom,
          left: 0,
          right: 0,
          height: 70,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ focused, color, size }) => {
            const iconName = focused ? 'home' : 'home-outline';
            return <Ionicons name={iconName} color={color} size={size} />;
          },
        }}
      />
      <Tab.Screen
        name="Entries"
        component={EntriesScreen}
        options={{
          tabBarIcon: ({ focused, color, size }) => {
            const iconName = focused ? 'calendar' : 'calendar-outline';
            return <Ionicons name={iconName} color={color} size={size} />;
          },
        }}
      />
      <Tab.Screen
        name="AddEntry"
        component={AddEntryScreen}
        options={{
          tabBarIcon: () => null, 
          tabBarButton: (props) => (
            <CustomTabBarButton 
              {...props} 
              // --- DÜZELTME 1 (ANA HATA) ---
              // Benim eklediğim 'onPress' satırını sildim.
              // 'props' zaten React Navigation'ın kendi 'onPress' fonksiyonunu
              // içeriyor ve CustomTabBarButton bunu 'handlePress' içinde
              // doğru şekilde (animasyon bitince) çağırıyor.
            />
          ),
        }}
      />
      <Tab.Screen
        name="Reports"
        component={ReportsScreen}
        options={{
          tabBarIcon: ({ focused, color, size }) => {
            const iconName = focused ? 'stats-chart' : 'stats-chart-outline';
            return <Ionicons name={iconName} color={color} size={size} />;
          },
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarIcon: ({ focused, color, size }) => {
            const iconName = focused ? 'person' : 'person-outline';
            return <Ionicons name={iconName} color={color} size={size} />;
          },
        }}
      />
    </Tab.Navigator>
  );
}

const styles = StyleSheet.create({
  shadow: {
    shadowColor: '#FFD54F',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 10,
  },
});