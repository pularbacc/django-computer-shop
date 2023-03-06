from django.shortcuts import render
from rest_framework.views import APIView
from product.models import *
from product.serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def getAll(product_name):
      data= {}
      _status= status.HTTP_200_OK
      try:
            if product_name== "Product":
                  list_items= Product.objects.all()
            else:
                  id_type= Product_Type.objects.get(name_type= product_name)
                  list_items= Product.objects.filter(product_type_id= id_type)
            data= ProductSerializer(list_items, many= True).data
      except:
            data['error']= 'An error has occur, type ' + str(product_name) + ' doesn\'t exist !!'
            _status = status.HTTP_400_BAD_REQUEST
      return Response(data, _status)

def getDetail(id_product):
      data= {}
      _status= status.HTTP_200_OK
      list_items= list_items= Product.objects.all()
      try:
            val= list_items.get(pk= id_product)
            data= ProductDetailSerializer(val).data
      except:
            data['error']= 'Product with id=' +str(id_product) + ' doesn\'t exist !!'
            _status = status.HTTP_400_BAD_REQUEST
      return Response(data, _status)


class getAllProductAPI(APIView):
      def get(self,request):
            return getAll("Product")


class getAllAPI(APIView):
      def get(self,request, type):
            return getAll(type)


class getProductDetailAPI(APIView):
      def get(self, request, id):
            return getDetail(id)


class getProductTypeAPI(APIView):
      def get(self, request):
            data= {}
            _list= Product_Type.objects.all()
            list_name= list(_list.values_list('name_type',flat=True))
            return Response(list_name,status.HTTP_200_OK)