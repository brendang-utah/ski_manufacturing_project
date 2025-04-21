from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Employee, Customer, Product, Order, OrderLine
from .serializers import (
    UserSerializer, EmployeeWriteSerializer, EmployeeReadSerializer,
    CustomerSerializer, ProductSerializer, OrderReadSerializer,
    OrderWriteSerializer, OrderLineSerializer
)

# API Views
class UserListPageView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    
    def get_serializer_class(self):
        return EmployeeWriteSerializer if self.request.method == 'POST' else EmployeeReadSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    
    def get_serializer_class(self):
        return EmployeeWriteSerializer if self.request.method == 'POST' else EmployeeReadSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/product-edit.html'
    success_url = '/products/'
#non-api version of order list
from django.views.generic import ListView

class OrderListPageView(LoginRequiredMixin, ListView):
    template_name = 'orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add order lines and product info to context
        orders_with_details = []
        for order in context['orders']:
            order_lines = OrderLine.objects.filter(order=order)
            orders_with_details.append({
                'order': order,
                'lines': order_lines
            })
        context['orders_with_details'] = orders_with_details
        return context

#api version of order list
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer

# Template Views
class HomepageView(TemplateView):
    template_name = 'ski_manufacturing_app/homepage.html'

class ProductListPageView(LoginRequiredMixin, TemplateView):
    template_name = 'products.html'

class ProductAddView(CreateView):
    model = Product
    fields = ['name', 'description', 'makeup', 'size', 'price', 'stock_status', 'imagepath']
    template_name = 'ski_manufacturing_app/add-product.html'
    success_url = '/products/'

@method_decorator(login_required, name='dispatch')
class BuyProductView(DetailView):
    model = Product
    template_name = 'buy_product.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = int(request.POST.get('quantity', 1))
        
        if not hasattr(request.user, 'customer'):
            return render(request, self.template_name, {
                'product': product,
                'error': 'You must have a customer profile to place an order.'
            })

        try:
            # Create order
            order = Order.objects.create(
                customer=request.user.customer,
                status='completed'
            )
            # Create order line
            OrderLine.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
                total_price=product.price * quantity
            )
            # Update stock
            product.stock_status -= quantity
            product.save()
            return redirect('order-page')
            
        except Exception as e:
            return render(request, self.template_name, {
                'product': product,
                'error': f'Order failed: {str(e)}'
            })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # Handle GET requests
    if request.method == 'GET':
        orders = Order.objects.filter(customer__user=request.user)
        order_data = []
        for order in orders:
            order_line = order.orderline_set.first()
            order_data.append({
                'id': order.id,
                'customer_name': order.customer.user.username,
                'product_name': order_line.product.name if order_line else "Unknown",
                'quantity': order_line.quantity if order_line else 0,
                'status': order.status,
                'date': order.date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return Response(order_data)

    # Handle POST requests
    elif request.method == 'POST':
        if not hasattr(request.user, 'customer'):
            return Response({'error': 'Customer profile required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))
            product = Product.objects.get(id=product_id)
            
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
