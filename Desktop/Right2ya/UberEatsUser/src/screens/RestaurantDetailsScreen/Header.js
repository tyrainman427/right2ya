
import {View, Image, Text} from 'react-native';
import restaurants from '../../../assets/data/restaurants.json';
import styles from './styles';


const RestaurantHeader = ({restaurant}) => {
    return (
        <View style={styles.page}>
            <Image source={{uri: restaurant.image}}  style={styles.image} resizeMode="cover" />

            <View style={styles.container}>
            <Text style={styles.title}>{restaurant.name}</Text>
            <Text style={styles.subtitle}>${restaurant.deliveryFee} &#8226; {restaurant.minDeliveryTime}-{restaurant.maxDeliveryTime} minutes</Text>
            </View>

            <Text style={styles.menuTitle}>Menu</Text>
        </View>
    );
    
};


export default RestaurantHeader;