from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/product-edit.html'
    success_url = '/products/'

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

#class buy_product:
class BuyProductView(DetailView):
    model = Product  # Specify the model to use
    template_name = 'buy_product.html'  # Specify the template to render
    context_object_name = 'product'  # Name of the object in the template
    # Define the URL pattern for this view
    def buy_product(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'GET':
            return render(request, 'buy_product.html', {'product': product})

'''
from django.http import JsonResponse

class BuyProductView(DetailView):
    def buy_product(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'GET':
            return render(request, 'buy_product.html', {'product': product})
        elif request.method == 'POST':
            data = json.loads(request.body)
            quantity = data.get('quantity')
            payment_details = data.get('payment_details')

            # Validate payment details (basic example)
            if not payment_details or not all(k in payment_details for k in ('card_number', 'exp_date', 'ccv')):
                return JsonResponse({'error': 'Invalid payment details'}, status=400)

            # Create the order
            order = Order.objects.create(
                product=product,
                user=request.user,
                quantity=quantity,
                payment_status='Paid'
            )
            return JsonResponse({'message': 'Order placed successfully', 'order_id': order.id}, status=201)
'''