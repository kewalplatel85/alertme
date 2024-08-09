"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fetch-messages/', views.fetch_messages, name='fetch_messages'),  # Endpoint to fetch chat messages
    path('send-reply/', views.send_reply, name='send_reply'),
    # path('send-reply/<str:sender>/', views.send_reply, name='send_reply'), 
    path('package-log/', views.package_log, name='package_log'),  
    path('update-log/', views.package_log, name='update_log'),
    path('custom_sms/', views.custom_sms, name='custom_sms'),
    path('', views.index, name='index'),
]
