# ski_manufacturing_app/template_urls.py
from django.urls import path
from .views import *

#these are all template urls go to the settings.py in project folder to see more info.
#all urls in this page start with products/ before the actual url listed. 
urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='home-page'),
    path('products/', ProductListPageView.as_view(), name='product-page'),
    path('products/add/', ProductAddView.as_view(), name='add-product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'), 
    path('orders', OrderListPageView.as_view(), name='order-page'),
    path('orders/<int:pk>/', OrderEditView.as_view(), name='order-edit'),
    path('orders/delete/<int:pk>/', OrderDeleteView.as_view(), name='delete-order'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('buy_product/<int:pk>/', BuyProductView.as_view(), name='buy_product'),
    path('users/', UserListPageView.as_view(), name='user-page'),
    path('users/add/', UserAddView.as_view(), name='add-user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('employees/', EmployeeListPageView.as_view(), name='employee-page'),
    path('employees/add/', EmployeeAddView.as_view(), name='add-employee'),
    path('employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee-edit'),
    path('raw-materials/', RawMaterialListPageView.as_view(), name='raw-materials-page'),
    path('raw-materials/add/', RawMaterialAddView.as_view(), name='add-raw-material'),
    path('raw-materials/<int:pk>/edit', RawMaterialUpdateView.as_view(), name='edit-raw-material'),
]
