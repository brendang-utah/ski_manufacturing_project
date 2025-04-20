"""
URL configuration for ski_manufacturing_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views #for handing simple auth on users



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ski_manufacturing_app.api_urls')),  # API endpoints see to-do for more info on this
    path('accounts/', include('django.contrib.auth.urls')), #login url
    path('', include('ski_manufacturing_app.template_urls')),  # Future non-API pages
    path('login/', auth_views.LoginView.as_view(), name='login'), #login url
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), #logout url WE DONT HAVE  ALOGOUT FUNCITON YET
]