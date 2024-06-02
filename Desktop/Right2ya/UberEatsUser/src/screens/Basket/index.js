import {useState} from 'react';
import { View, Text, StyleSheet } from "react-native";
import {AntDesign} from '@expo/vector-icons';
import restaurants from '../../../assets/data/restaurants.json';

const restaurant = restaurants[0];

const Basket = () => {
    const [quantity, setQuantity] = useState(3);

    const onMinus = () => {
        if (quantity > 1) {
            setQuantity(quantity - 1)
        }
       
    }

    const onPlus = () => {
        setQuantity(quantity + 1)
    }
    
    const getTotal = () => {
        // return (dish.price * quantity).toFixed(2)
    }

    return (
        <View style={styles.page}>
            <Text style={styles.name}>{restaurant.name}</Text>
            <Text style={styles.items}>Your Items</Text>

            <View style={styles.row}>
                <View style={styles.quantityContainer}>
                    <Text>1</Text>
                </View>
                <Text style={{fontWeight:'600'}}>Name</Text>
                <Text style={{marginLeft:'auto'}}>$12</Text>
            </View>

            <View style={styles.separator} />

            <View style={styles.button}>
                <Text style={styles.buttonText}>Create Order</Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    page: {
        flex:1,
        width: '100%',
        paddingVertical:30,
    },
    description:{
        color:'gray'
    },
    name:{
        fontSize:25,
        fontWeight:'600',
        marginVertical:10,
    },
    separator: {
        height:1,
        backgroundColor: 'lightgrey',
        marginVertical:10,
    },
    row: {
        flexDirection:'row',
        alignItems:'center',
        marginTop:50,
    },
    quantity: {
        fontSize:25,
        marginHorizontal:20,
    },
    button: {
        backgroundColor:'black',
        marginTop:'auto',
        padding:20,
        alignItems:'center'
    },
    buttonText: {
        color:'white',
        fontWeight:'600',
        fontSize:18,
    },
    quantityContainer: {
        backgroundColor:'lightgray',
        paddingHorizontal:5,
        marginRight:10,
        paddingVertical:2,
        borderRadius:3
    },
});

export default Basket;