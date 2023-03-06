from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from user.models import Customer
from user.serializers import *

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegistrationAPI(APIView):
      def post(self,request):
            serializers= RegistrationSerializers(data=request.data)
            data= {}
            _status= status.HTTP_200_OK
            if serializers.is_valid():
                  account= serializers.save()
                  refresh= RefreshToken.for_user(account)
                  data['refresh']= str(refresh)
                  data['access']= str(refresh.access_token)
            else:
                  data= serializers.errors
                  _status= status.HTTP_400_BAD_REQUEST
            return Response(data,_status)

class getUserInforAPI(APIView):
      permission_classes=[permissions.IsAuthenticated]

      def get(self,request):
            infor= Customer.objects.get(pk=request.user.id)
            data= {}
            _status= status.HTTP_200_OK
            try:
                  data= getUserInforSerializers(infor).data
            except:
                  data["error"]= "an error has occur"
            return Response(data,_status)

class refreshPasswordAPI(APIView):
      def post(self, request):
            data= {}
            _status= status.HTTP_200_OK
            data_input= request.data
            _customer= Customer.objects.get(username= data_input.get('username'))
            if _customer.email != data_input.get('email'):
                  data['error']= 'email must match!'
                  _status= status.HTTP_400_BAD_REQUEST
            elif data_input.get('password') != data_input.get('password2'):
                  data['error']= 'passwords must match!'
                  _status= status.HTTP_400_BAD_REQUEST
            else:
                  _customer.set_password(data_input.get('password'))
                  _customer.save()
                  refresh= RefreshToken.for_user(_customer)
                  data['refresh']= str(refresh)
                  data['access']= str(refresh.access_token)
            return Response(data,_status)


class updateUserInforAPI(APIView):
      permission_classes=[permissions.IsAuthenticated]

      def post(self, request):
            data= {}
            _status= status.HTTP_200_OK
            data_input= request.data
            _customer= request.user

            try:
                  _customer.first_name= data_input.get('first_name')
                  _customer.last_name= data_input.get('last_name')
                  _customer.address= data_input.get('address')
                  _customer.phone_number= data_input.get('phone_number')
                  _customer.save()

                  data= getUserInforSerializers(_customer).data
            except:
                  data['error']= 'An error has occurr!'
                  _status= status.HTTP_400_BAD_REQUEST

            return Response(data,_status)

class updateEmailAPI(APIView):
      permission_classes=[permissions.IsAuthenticated]

      def post(self, request):
            data= {}
            _status= status.HTTP_200_OK
            data_input= request.data
            _customer= request.user

            try:
                  _customer.email= data_input.get('email')
                  _customer.save()

                  data= getUserInforSerializers(_customer).data
            except:
                  data['error']= 'An error has occurr!'
                  _status= status.HTTP_400_BAD_REQUEST

            return Response(data,_status)