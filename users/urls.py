from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('dashboard/', views.dashboard,  name='dashboard'), 
    path('login/', views.login, name='login'),
    path('logout', views.logout_request, name='logout'),
]