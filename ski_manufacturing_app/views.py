from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from rest_framework.authentication import SessionAuthentication

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
        return request.user.is_staff
    
    
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

class ProductListPageView(LoginRequiredMixin, TemplateView):
    template_name = 'products.html'

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication]  # Enforce session auth
    permission_classes = [permissions.IsAdminUser]  # Restrict to admins
    
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/product-edit.html'
    success_url = '/products/'


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
    serializer_class = OrderReadSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    
class OrderListPageView(LoginRequiredMixin, TemplateView):
    template_name = 'orders.html'

# OrderLine Views
class OrderLineListCreateView(generics.ListCreateAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

class OrderLineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer





#def HomepageView(TemplateView): 
class HomepageView(TemplateView):
    template_name = 'ski_manufacturing_app/homepage.html'

#def PrudoctCreate(ProductView):
class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/product-create.html'
    success_url = '/products/'

#def ProductList(ListView):
class ProductDetail(DetailView):
    model = Product
    template_name = 'ski_manufacturing_app/product-detail.html'
    context_object_name = 'product'

#class ProductDetail(DetailView):
class ProductDetail(DetailView):
    model = Product
    template_name = 'ski_manufacturing_app/product-detail.html'
    context_object_name = 'product'

#def OrderCreate(CreateView):
class OrderCreate(CreateView):
    model = Order
    fields = ['customer', 'payment', 'status']
    template_name = 'ski_manufacturing_app/order-create.html'
    success_url = '/orderlist'

#class OrderDetail(DetailView):
class OrderDetail(DetailView):
    model = Order
    template_name = 'ski_manufacturing_app/order-detail.html'
    context_object_name = 'order'

 