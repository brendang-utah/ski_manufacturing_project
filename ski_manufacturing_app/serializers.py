from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Employee, Customer, Product, Order, OrderLine, RawMaterial


#serializers
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Allow blank for updates
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance



        

# Use this for WRITE operations (creating/updating employees)
class EmployeeWriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    position = serializers.CharField()
    training_status = serializers.BooleanField()

    class Meta:
        model = Employee
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'position', 'training_status']

    @transaction.atomic
    def create(self, validated_data):
        # Extract user-related fields
        user_fields = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
        }

        # Create the User instance first
        user = User.objects.create_user(**user_fields)
        
        # Create the Employee instance
        employee = Employee.objects.create(
            user=user,
            position=validated_data['position'],
            training_status=validated_data['training_status']
        )
        
        return employee

# Use this for READ operations (listing employees)
class EmployeeReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested read-only


    class Meta:
        model = Employee
        fields = ['user', 'position', 'training_status']
        
        
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderLine
        fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price']

class OrderWriteSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True, source='orderline_set')

    class Meta:
        model = Order
        fields = ['customer', 'status', 'order_lines']
        read_only_fields = ['status']

    def create(self, validated_data):
        order_lines_data = validated_data.pop('order_lines')
        order = Order.objects.create(**validated_data)
        
        for line_data in order_lines_data:
            product = line_data['product']
            OrderLine.objects.create(
                order=order,
                **line_data
            )
            product.stock_status -= line_data['quantity']
            product.save()
        return order

class OrderReadSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.username')
    order_lines = OrderLineSerializer(many=True, source='orderline_set')
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'date', 'customer_name', 'order_lines']


class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'




