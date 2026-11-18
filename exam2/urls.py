from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', register, name='register'),
    path('login/', loginn, name='loginn'),
    path('logout/', logout_user, name='logout'),
]
