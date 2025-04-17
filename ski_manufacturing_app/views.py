from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin 

# API Views
# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Employee Views
class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'
    
    
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    
    def get_serializer_class(self):
            # Use WriteSerializer for POST, ReadSerializer for GET
            return EmployeeWriteSerializer if self.request.method == 'POST' else EmployeeReadSerializer
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        # Use WriteSerializer for POST, ReadSerializer for GET
        return EmployeeWriteSerializer if self.request.method == 'POST' else EmployeeReadSerializer

# Customer Views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Product Views
class ProductListCreateView(LoginRequiredMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEmployee()]
        return super().get_permissions()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsEmployee()]

# RawMaterial Views
class RawMaterialListCreateView(generics.ListCreateAPIView):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer

class RawMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer

# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# OrderLine Views
class OrderLineListCreateView(generics.ListCreateAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

class OrderLineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

# Report Views
# class ReportListCreateView(generics.ListCreateAPIView):
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer

# class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer

# Return Views
class ReturnListCreateView(generics.ListCreateAPIView):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer

class ReturnDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer



#def HomepageView(TemplateView): 


#def PrudoctCreate(ProductView):


#def ProductList(ListView):


#class ProductDetail(DetailView):


#def OrderCreate(CreateView):


#class OrderDetail(DetailView):
 

 