from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.booklist, name = 'booklist'),
    path('order/',views.orderlist, name = 'orderlist'),
    path('modify/',views.modify, name = 'modify'),
    path('profile/',views.profile, name = 'profile')
]