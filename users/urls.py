# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('loggedin', views.my_view, name='my_view'),
    path('<str:username>', views.profile, name='profile'),
]