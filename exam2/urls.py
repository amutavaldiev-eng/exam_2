from django.urls import path
from .views import *

urlpatterns = [
    path("",home, name='home'),

    path('register/',register, name='register'),
    path('login/',loginn, name='loginn'),
    path('logout/',logout_user, name='logout_user'),
    path('fields/',fields, name='fields'),
    path('fields/<int:id>/',show_fields, name='show_fields'),
    path('fields/<int:id>/book/',book_field, name='book_field'),
    path('my-fields/',my_fields, name='my_fields'),
    path('bookings/<int:id>/',booking_detail, name='booking_detail'),
    path('bookings/<int:id>/cancel/',cancel_booking, name='cancel_booking'),
    path('bookings/<int:id>/finish/',finish_booking, name='finish_booking'),
    path('play-together/',play_together, name='play_together'),
    path('bookings/<int:id>/join/',join_team, name='join_team'),
    path('bookings/<int:id>/leave/',leave_team, name='leave_team'),
    path('profile/',profile, name='profile'),
    path('profile/edit/',update_profile, name='update_profile'),
]