from django.shortcuts import render
from  django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status

import hmac
import hashlib
import json
from django.http import HttpResponse

from .models import Product, UserProfile , Cart,  Order

from .Appserializer import Productserializer, Userserializer, Cartserializer, Orderserializer, Vtuserializer


def Home(request):

    return render(request, "build/index.html", {})

@api_view(["POST"])
def Register_user(request):
    if request.method == "POST":
        register = Userserializer(data=request.data)
        if register.is_valid():
            register.save()
            return Response(register.data, status= status.HTTP_200_OK)
    return Response(register.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def Update_user(request,id):
    if request.method == "POST":
        db_query = UserProfile.objects.get(user_id=id)
        user_info = Userserializer(db_query, many= True)
        db_query.wallet = request.data.get("wallet", db_query.wallet)
        db_query.phone  = request.data.get("phone", db_query.phone )
        db_query.password = request.data.get("password", db_query.password)
        db_query.email = request.data.get("email", db_query.email)
        db_query.name = request.data.get("name", db_query.password)
        user_info = {
                    "user_id" : db_query.user_id,
                    "name" :  db_query.name,
                    "wallet" : db_query.wallet,
                    "email" : db_query.email,
                    "phone" : db_query.phone,
                    "name"  : db_query.name
                }
        db_query.save()
        return Response(user_info, status= status.HTTP_200_OK)
    return Response(user_info, status= status.HTTP_400_BAD_REQUEST)

@api_view(["POST", "GET"])
def Orders(request, id):
    error = { data : "could not complete your request"}
    if request.method == "POST" :
        user = UserProfile.objects.get(user_id = id)
        order= Orderserializer(data =request.data)
        order_item = request.data.get("order_item")
        total_price = request.data.get("total_price")
        print("from front end", total_price, order_item)
        cart = user.order_id.create(
            item_order=order_item,
            user_id = user.user_id,
            total_price = total_price
        )
        all_cart = user.order_id.all()
        return Response(all_cart.values(), status= status.HTTP_200_OK)
    elif request.method == "GET":
        all_item = user.order_id.all()
        return Response(all_item.values(), status= status.HTTP_200_OK)
    return Response(error, status= status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
def Vtu_record(request, id):
    error = { "message" : "could not complete your request"}
    if request.method == "POST" :
        user = UserProfile.objects.get(user_id = id)
        #order = Vtuserializer(data=request.data)
        ref_id = request.data.get("ref_id")
        amount = request.data.get("amount")
        phone = request.data.get("phone")
        transaction_type = request.data.get("transaction_type")
        vtu = user.vtu_id.create(
            ref_id=ref_id,
            amount = amount,
            transaction_type=transaction_type,
            phone = phone
        )
        all_cart = user.vtu_id.all()
        return Response(all_cart.values(), status= status.HTTP_200_OK)
    elif request.method == "GET":
        all_item = user.vtu_id.all()
        return Response(all_item.values(), status= status.HTTP_200_OK)
    return Response(error, status= status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Login_user(request):
    error = {"message": "User Info does not Exist Or Wrong Data"}
    if request.method == "POST":
        user_data = Userserializer(data= request.data)
        password = (user_data.initial_data["password"])
        email = user_data.initial_data["email"]
        db_query = UserProfile.objects.get(email=email)
        if db_query:
            if ((db_query.password) == (password)):
                user_info = {
                    "user_id" : db_query.user_id,
                    "name" :  db_query.name,
                    "wallet" : db_query.wallet,
                    "email" : db_query.email,
                    "phone" : db_query.phone
                }
                return Response(user_info, status= status.HTTP_200_OK)
        else:
            return Response(error, status= 300)
    return Response(error, status= 303)


@api_view(["GET"])
def GetProduct( request):
    if request.method == "GET":
        get_product = Product.objects.all()
        product = Productserializer(get_product, many=True)
        return Response(product.data, status= status.HTTP_200_OK)
    return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)



class Post_product(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        product = Productserializer(data=request.data)
        if product.is_valid():
            product.save()
            return Response(product.data, status= status.HTTP_200_OK)
        return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def GetMenCategory(request):
    if request.method == "GET":
        data = Product.objects.filter(product_category = "MEN")
        men = Productserializer(data, many=True)
        return Response(men.data, status= status.HTTP_200_OK)
    return Response(men.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def GetWomenCategory(request):
    if request.method == "GET":
        data = Product.objects.filter(product_category = "WOMEN")
        women = Productserializer(data, many=True)
        return Response(women.data, status= status.HTTP_200_OK)
    return Response(women.errors, status= status.HTTP_400_BAD_REQUEST)



@api_view(["POST", "GET"])
def Payment(request):
    error = { "message" : "could not complete your request"}
    #output = json.loads(pay)
    Payment_info = request.data
    customer_data = pay['data']['customer']
    transaction_info = pay['data']
    email = customer_data['email']
    amount = transaction_info['amount']
    reference = transaction_info['reference']
    transaction_time = transaction_info['paid_at']
    user_info = UserProfile.objects.get(email=email)
    transaction_type = "PAYSTACK FUNDING"
    vtu = user_info.vtu_id.create(
        ref_id = reference,
        amount = amount,
        transaction_time = transaction_time,
        transaction_type = transaction_type
    )
    all_cart = user_info.vtu_id.all()
    return Response(all_cart.values(), status= status.HTTP_200_OK)

    return Response(error, status= status.HTTP_400_BAD_REQUEST)

