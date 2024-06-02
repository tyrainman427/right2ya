import { StatusBar } from 'expo-status-bar';
import { StyleSheet,View} from 'react-native';
import DishDetailsScreen from './src/screens/DishDetailsScreen';
import HomeScreen from './src/screens/HomeScreen';
import RestaurantDetailsPage from './src/screens/RestaurantDetailsScreen';
import Basket from './src/screens/Basket';

export default function App() {
  return (
   <View style={styles.container}>
     {/* <DishDetailsScreen /> */}
     <Basket />

    <StatusBar style="light" />
  </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
