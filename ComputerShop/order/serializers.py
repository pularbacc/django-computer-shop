from rest_framework import serializers
from product.serializers import ProductSerializer, ProductDetailSerializer
from order.models import *


class addToCartSerializer(serializers.ModelSerializer):
      
      class Meta:
            model= Cart
            fields =(
                  'customer',
                  'product',
            )

      def save(self):
            _customer= self.validated_data['customer']
            _product= self.validated_data['product']
            
            c = Cart.objects.filter(customer_id= _customer.id, product_id= _product.id)
            count= 0
            if c.exists():
                  cart=c.get()
                  count= cart.number_product
                  print(cart.number_product)
            p_count= _product.Available_Quantity
            if p_count == 0:
                  raise serializers.DjangoValidationError({'product':'The product is out of stock'})
            if p_count<= count:
                  raise serializers.DjangoValidationError({'product':'All products have been added'})
            # check all success
            if c.exists():
                  cart=c.get()
                  cart.number_product+= 1
                  cart.save()
            else:
                  cart = Cart(
                        customer= _customer,
                        product= _product,
                        number_product= 1
                  )
                  cart.save()
            return ProductDetailSerializer(Product.objects.get(pk= _product.id)).data


class removeFromCartSerializer(serializers.ModelSerializer):

      class Meta:
            model= Cart
            fields = '__all__'

      def save(self):
            _customer= self.validated_data['customer']
            _product= self.validated_data['product']
            _amount= self.validated_data['number_product']

            cart_item= Cart.objects.filter(customer_id= _customer.id, product_id= _product.id)

            if cart_item.exists():
                  cart=cart_item.get()
                  if _product.Available_Quantity == 0:
                        cart_item.delete()
                        return True
                  elif cart.number_product- _amount== 0:
                        cart_item.delete()
                        return True
                  elif cart.number_product- _amount> 0:
                        cart.number_product-= _amount
                        cart.save()
                        return True
                  else:
                        raise serializers.DjangoValidationError({'error':'The number of product you entered is invalid!'})
            else:
                  raise serializers.DjangoValidationError({'error':'Your cart does not contain this product!'}) 


class getCartItemsSerializer(serializers.ModelSerializer):
      product= serializers.SerializerMethodField(read_only=True)
      
      class Meta:
            model= Cart
            fields =(
                  'product',
                  'number_product',
            )

      def get_product(self,obj):
            try:
                  return ProductSerializer(obj.product).data
            except:
                  return None


class getOrderSerializer(serializers.ModelSerializer):
      payment= serializers.SerializerMethodField(read_only=True)
      class Meta:
            model= Orders
            fields =(
                  'id',
                  'order_date',
                  'total_prices',
                  'payment',
            )
      
      def get_payment(self, obj):
            return obj.payment.payment_type


class getOrderDetailSerializer(serializers.ModelSerializer):
      name_customer= serializers.SerializerMethodField(read_only=True)
      payment= serializers.SerializerMethodField(read_only=True)
      list_product= serializers.SerializerMethodField(read_only=True)
      
      class Meta:
            model= Orders
            fields =(
                  'name_customer',
                  'delivery_address',
                  'order_date',
                  'list_product',
                  'total_prices',
                  'payment',
            )
      
      def get_payment(self, obj):
            return obj.payment.payment_type

      def get_name_customer(self, obj):
            try: 
                  return str(obj.customer.first_name)+" "+ str(obj.customer.last_name)
            except:
                  return None

      def get_list_product(self, obj):
            data= []
            order_details= Orders_detail.objects.filter(orders_id= obj.id)
            _dict= dict(order_details.values_list('product', 'number_product'))
            for i in _dict:
                  data_item= {}
                  data_item['product'] = ProductSerializer(Product.objects.get(pk=i)).data
                  data_item['number_product']= _dict.get(i)
                  data.append(data_item)
            return data


class AddNewOrderSerializer(serializers.ModelSerializer):
      
      class Meta:
            model= Orders
            fields =(
                  'customer',
                  'delivery_address',
                  'payment',
            )

      def save(self,):
            _customer= self.validated_data['customer']
            _delivery_address= self.validated_data['delivery_address']
            _payment= self.validated_data['payment']
            _total_prices= 0
            # Kiểm tra tên người nhận 
            if _customer.first_name=='' or _customer.last_name== '':
                  raise serializers.DjangoValidationError({'error':'Customer\'s name is required!'})
            if _customer.phone_number== '':
                  raise serializers.DjangoValidationError({'error':'Customer\'s phone number is required!'})
            # Kiểm tra địa chỉ nhận 
            if _delivery_address=='': 
                  if _customer.address== '':
                        raise serializers.DjangoValidationError({'error':'Delivery address is required!'})
                  else:
                        _delivery_address= _customer.address
            # Kiểm tra hình thức thanh toán có hỗ trợ không 
            if not _payment.available:
                  raise serializers.DjangoValidationError({'error':'Payment not support!'})
            # Kiểm tra giỏ hàng có sp không 
            cart= Cart.objects.filter(customer_id= _customer.id)
            if cart.exists():
                  list_cart_items_amount = dict(cart.values_list('product', 'number_product'))
                  products= Product.objects.filter(pk__in= list_cart_items_amount.keys())
                  print(products)
                  # Kiểm tra xem sp còn hàng không
                  for i in range( len(products)):
                        if products[i].Available_Quantity- list_cart_items_amount.get( products[i].id) < 0:
                              raise serializers.DjangoValidationError({'error':'Some of products you order is out of range'})
                  # Giảm số lượng sp 
                  for i in range( len(products)):
                        products[i].Available_Quantity -= list_cart_items_amount.get( products[i].id)
                        products[i].save()
                  # Tạo order 
                  _order = Orders(
                        customer= _customer, 
                        delivery_address= _delivery_address,
                        payment= _payment
                  )
                  _order.save()
                  # Tạo order_detail
                  for i in list_cart_items_amount:
                        p= Product.objects.get(pk=i)
                        order_detail= Orders_detail(
                              orders= _order,
                              product= p,
                              number_product= list_cart_items_amount.get(i),
                              price= p.price* list_cart_items_amount.get(i)
                        )
                        order_detail.save()
                        _total_prices+= p.price*list_cart_items_amount.get(i)
                  # update giá tổng 
                  _order.total_prices= _total_prices
                  _order.save()
                  # Xóa hết item trong cart
                  cart.delete()
                  return getOrderDetailSerializer(_order).data
            else:
                  raise serializers.DjangoValidationError({'error':'Your cart is empty!'})