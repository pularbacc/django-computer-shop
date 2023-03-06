from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from order.models import *
from .serializers import *

# Create your views here.


class addToCartAPI(APIView):
      permission_classes= [permissions.IsAuthenticated]

      def post(self, request, id_product):
            data={}
            data_input={}
            data_input["customer"]= request.user.id
            _status= status.HTTP_200_OK
            data_input["product"]= id_product
            serializers= addToCartSerializer(data= data_input)
            if serializers.is_valid():
                  try:
                        data["product"]=serializers.save()
                  except ValidationError as err:
                        data= err
                        _status= status.HTTP_400_BAD_REQUEST
            else:
                  data= serializers.errors
                  _status= status.HTTP_400_BAD_REQUEST
            return Response(data,_status)


class removeFromCart(APIView):
      permission_classes= [permissions.IsAuthenticated]

      def delete(self, request):
            data= {}
            _status= status.HTTP_200_OK
            data_input= {}
            data_input["customer"] = request.user.id
            data_input.update(request.data)

            val= removeFromCartSerializer(data=data_input)
            if val.is_valid():
                  try:
                        response = val.save()
                        cart_items = Cart.objects.filter(customer_id= request.user.id)
                        data= getCartItemsSerializer(cart_items,many=True).data
                  except ValidationError as err:
                        data= err
                        _status= status.HTTP_400_BAD_REQUEST
            
            return Response(data,_status)


class getCartItemsAPI(APIView):
      permission_classes= [permissions.IsAuthenticated]

      def get(self, request):
            cart_items = Cart.objects.filter(customer_id= request.user.id)
            data= getCartItemsSerializer(cart_items,many=True).data
            return Response(data,status.HTTP_200_OK)


class getOrdersAPI(APIView):
      permission_classes=[permissions.IsAuthenticated]

      def get(self, request):
            list= Orders.objects.filter(customer_id=request.user.id)
            data={}
            _status= status.HTTP_200_OK
            data= getOrderSerializer(list,many=True).data
            return Response(data,_status)


class getOrderDetailAPI(APIView):
      permission_classes=[permissions.IsAuthenticated]

      def get(self, request, id_order):
            list= Orders.objects.filter(customer_id=request.user.id)
            data={}
            _status= status.HTTP_200_OK
            try:
                  d= list.get(pk=id_order)
                  data= getOrderDetailSerializer(d).data
            except:
                  data['error']= 'Orders does not exist'
                  _status= status.HTTP_400_BAD_REQUEST
            return Response(data,_status)


class addNewOrderAPI(APIView):
      permission_classes= [permissions.IsAuthenticated]

      def post(self, request):
            data= {}
            _status= status.HTTP_200_OK
            data_input= {}
            data_input["customer"] = request.user.id
            data_input.update(request.data)

            val= AddNewOrderSerializer(data=data_input)
            if val.is_valid():
                  try:
                        data = val.save()
                  except ValidationError as err:
                        data= err
                        _status= status.HTTP_400_BAD_REQUEST
            
            return Response(data,_status)