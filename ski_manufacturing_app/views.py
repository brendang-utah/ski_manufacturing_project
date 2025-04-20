from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import requests  # Used in BuyProductView.post

from .models import *
from .serializers import *
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

# add product view:
class ProductAddView(CreateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/add-product.html'
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
    
#order create for BUY_PRODUCT


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        # Get product info
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = Product.objects.get(id=product_id)
        
        # Create order data without payment
        order_data = {
            "customer": request.user.customer.id,
            "status": "completed",
            "order_lines": [{
                "product": product_id,
                "quantity": quantity,
                "unit_price": str(product.price),
                "total_price": str(product.price * quantity)
            }]
        }

        serializer = OrderWriteSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



#class OrderDetail(DetailView):
class OrderDetail(DetailView):
    model = Order
    template_name = 'ski_manufacturing_app/order-detail.html'
    context_object_name = 'order'

# #class buy_product:
# class BuyProductView(DetailView):
#     model = Product  # Specify the model to use
#     template_name = 'buy_product.html'  # Specify the template to render
#     context_object_name = 'product'  # Name of the object in the template
#     # Define the URL pattern for this view
#     def buy_product(request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         if request.method == 'GET':
#             return render(request, 'buy_product.html', {'product': product})
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class BuyProductView(DetailView):
    model = Product
    template_name = 'buy_product.html'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            response = requests.post(
                'http://localhost:8000/api/orders/',
                json={
                    "product_id": product.id,
                    "quantity": quantity
                },
                headers={
                    'X-CSRFToken': request.COOKIES.get('csrftoken'),
                    'Content-Type': 'application/json'
                },
                cookies=request.COOKIES
            )
            
            if response.status_code == 201:
                return redirect('order-confirmation')
            
            return render(request, self.template_name, {
                'error': response.json().get('error', 'Order failed'),
                'product': product
            })
            
        except Exception as e:
            return render(request, self.template_name, {
                'error': str(e),
                'product': product
            })

        
        # Call order creation API
        response = create_order(request._request)
        if response.status_code == 201:
            return redirect('order-confirmation')
        return render(request, 'buy_product.html', {'error': 'Order failed'})
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