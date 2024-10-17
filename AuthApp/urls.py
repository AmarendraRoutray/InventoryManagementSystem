from django.urls import path
from AuthApp import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
]
