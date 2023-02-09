from rest_framework import serializers
from core.models import Customer, Service, Customer, Courier, Order, OrderDetails

class CustomerSerializer(serializers.ModelSerializer):
  logo = serializers.SerializerMethodField()

  def get_logo(self, restaurant):
    request = self.context.get('request')
    logo_url = restaurant.logo.url
    return request.build_absolute_uri(logo_url)

  class Meta:
    model = Customer
    fields = ("id", "name", "phone", "address", "logo")


class ServiceSerializer(serializers.ModelSerializer):
  image = serializers.SerializerMethodField()

  def get_image(self, restaurant):
    request = self.context.get('request')
    image_url = Customer.avatar
    return request.build_absolute_uri(image_url)

  class Meta:
    model = Service
    fields = ("id", "name", "short_description", "image", "price")


# ORDER SERIALIZER

class OrderCustomerSerializer(serializers.ModelSerializer):
  name = serializers.ReadOnlyField(source="user.get_full_name")

  class Meta:
    model = Customer
    fields = ("id", "name", "avatar", "address")


class OrderDriverSerializer(serializers.ModelSerializer):
  name = serializers.ReadOnlyField(source="user.get_full_name")

  class Meta:
    model = Courier
    fields = ("id", "name", "avatar", "car_model", "plate_number")

class OrderRestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ("id", "name", "phone", "address")

class OrderMealSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = ("id", "name", "price")

class OrderDetailsSerializer(serializers.ModelSerializer):
  meal = OrderMealSerializer()
  class Meta:
    model = OrderDetails
    fields = ("id", "meal", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
  customer = OrderCustomerSerializer()
  driver = OrderDriverSerializer()
  restaurant = OrderRestaurantSerializer()
  order_details = OrderDetailsSerializer(many=True)
  status = serializers.ReadOnlyField(source="get_status_display")

  class Meta:
    model = Order
    fields = ("id", "customer", "restaurant", "driver", "order_details", "total", "status", "address")

class OrderStatusSerializer(serializers.ModelSerializer):
  status = serializers.ReadOnlyField(source="get_status_display")

  class Meta:
    model = Order
    fields = ("id", "status")
