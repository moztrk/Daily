// navigation/AppNavigator.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import LoginScreen from '../screens/LoginScreen';
import SignUpScreen from '../screens/SignUpScreen';
import MainTabNavigator from './MainTabNavigator';
import EntryDetailScreen from '../screens/EntryDetailScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false, // Üstteki başlık çubuğunu gizle
        }}
      >
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="SignUp" component={SignUpScreen} />
        <Stack.Screen name="Main" component={MainTabNavigator} />
        <Stack.Screen name="EntryDetail" component={EntryDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}