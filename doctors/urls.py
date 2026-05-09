from django.urls import path
from . import views

urlpatterns = [
    #client
    path('doctors/', views.get_doctors),
    path('bookings/create/', views.create_booking),
    path('slots/<int:doctor_id>/', views.get_slots),

    #doctor
    path('doctor/login/', views.doctor_login),
    path('doctor/slots/add/', views.add_slot),
    path('doctor/bookings/<int:doctor_id>/', views.get_my_bookings),
]