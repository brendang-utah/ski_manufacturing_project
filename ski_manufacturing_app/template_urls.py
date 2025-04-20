# ski_manufacturing_app/template_urls.py
from django.urls import path
from .views import *

#these are all template urls go to the settings.py in project folder to see more info.
#all urls in this page start with products/ before the actual url listed. 
urlpatterns = [
    path('products/', ProductListPageView.as_view(), name='product-page'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'), #go to settings.py and fix these urls so order list can just be /orderlist 
    path('orderlist', OrderListPageView.as_view(), name='order-page'),
    path('homepage', HomepageView.as_view(), name='home-page'), 
]
