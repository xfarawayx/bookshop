from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('bookManage/', views.bookManage, name = 'bookManage'),
    path('bookEdit/<str:bnum>/', views.bookEdit, name = 'bookEdit'),
    path('bookAdd/', views.bookAdd, name = 'bookAdd'),
    path('bookDelete/', views.bookDelete, name = 'bookDelete'),
    path('userManage/', views.userManage, name = 'userManage'),
    path('userManage/userOrder/<str:num>/', views.userOrder, name = 'userOrder'),
    path('userManage/userEdit/<str:num>/', views.userEdit, name = 'userEdit'),
    path('userVerify/', views.userVerify, name = 'userVerify'),
    path('userReset/', views.userReset, name = 'userReset'),
    path('selfModify/', views.selfModify, name = 'selfModify')
]