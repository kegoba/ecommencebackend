from rest_framework import serializers
from .models import Product, UserProfile, Cart, Order, Vtu_transaction



class Productserializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ["product_id", "product_price", "product_category", "image", "product_desc" ] 



class Userserializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields = ["wallet", "name", "password", "email", "phone" ] 


class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model= Cart
        fields = ["id", "item", "user_id"]

class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = ["id", "item_order", "user_id"]

class Vtuserializer(serializers.ModelSerializer):
    class Meta:
        model= Vtu_transaction
        fields = ["id", "transaction_type","phone", "ref_id", "amount", "user_id", "transaction_time"]
