from django.urls import path
from . import views


# this is a URL conf which basically means URL configuration
urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.studentlogin, name='login'),
    path('logout/',views.studentlogout, name='logout'),
    path('anxiety/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('advice/', views.advice, name='advice'),
    path('getResponse/', views.getResponse, name = 'getResponse'),
    
]