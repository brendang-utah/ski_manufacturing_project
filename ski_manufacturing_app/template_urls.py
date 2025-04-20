# ski_manufacturing_app/template_urls.py
from django.urls import path
from .views import *

#these are all template urls go to the urls.py in project folder to see more info.
#all urls in this page start with products/ before the actual url listed. 
urlpatterns = [
    path('list', ProductListPageView.as_view(), name='product-page'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orderlist', OrderListPageView.as_view(), name='order-page'),
]
