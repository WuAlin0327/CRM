from django.contrib import admin
from django.urls import path,include
from stark.service.stark import site
from management.views.login import *

urlpatterns = [
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('index/',index,name='index')
]