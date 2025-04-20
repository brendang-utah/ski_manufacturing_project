from rest_framework import serializers
from .models import Employee, Customer, Product, Order, OrderLine
from django.contrib.auth.models import User


#serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        

# Use this for WRITE operations (creating/updating employees)
class EmployeeWriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)
    
    class Meta:
        model = Employee
        fields = ['username', 'password', 'position', 'training_status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)  # Create User first
        return Employee.objects.create(user=user, **validated_data)

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

class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'payment', 'status']

class OrderLineSerializer(serializers.ModelSerializer):
    order = OrderReadSerializer() # Use OrderReadSerializer for read-only fields
    product = ProductSerializer()
    class Meta:
        model = OrderLine
        fields = '__all__'


