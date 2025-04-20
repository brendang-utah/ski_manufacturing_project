from django.urls import path
from .views import *

# API URLs
urlpatterns = [
    # User
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Employee
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Customer
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Product
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),


    # Payment
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    # Order
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # OrderLine
    path('orderlines/', OrderLineListCreateView.as_view(), name='orderline-list-create'),
    path('orderlines/<int:pk>/', OrderLineDetailView.as_view(), name='orderline-detail'),


]
