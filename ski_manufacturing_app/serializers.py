from rest_framework import serializers
from .models import User, Employee, Customer, Product, RawMaterial, Payment, Order, OrderLine, Report, Return

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    payment = PaymentSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class OrderLineSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()
    class Meta:
        model = OrderLine
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    employee = EmployeeSerializer()
    class Meta:
        model = Report
        fields = '__all__'

class ReturnSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()
    class Meta:
        model = Return
        fields = '__all__'