from rest_framework import serializers
from user.models import Customer


class RegistrationSerializers(serializers.ModelSerializer):
      password2= serializers.CharField(style={'input_type':'password'}, write_only=True)

      class Meta:
            model= Customer
            fields= ('email','username','password','password2')
            extra_kwargs= {
                  'password' : {'write_only' : True}
            }
      
      def save(self):
            account= Customer(
                  email=self.validated_data['email'],
                  username= self.validated_data['username'],
            )
            password= self.validated_data['password']
            password2= self.validated_data['password2']
            
            if password != password2:
                  raise serializers.ValidationError({'password':'passwords must match'})

            account.set_password(password)
            account.save()
            
            return account


class getUserInforSerializers(serializers.ModelSerializer):

      class Meta:
            model= Customer
            fields=(
                  'id',
                  'first_name',
                  'last_name',
                  'email',
                  'is_superuser',
                  'address',
                  'phone_number'
            )