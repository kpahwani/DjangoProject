from django.urls import path,re_path
from . import views

app_name = "manage_profile"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.login, name='home'),
    path('register/', views.resigter, name='register'),
    path('sign_up/', views.sign_up, name='sign_up'),
]
