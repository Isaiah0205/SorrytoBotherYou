from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name = "login"),
    path("register/", views.registerPage, name = "register"),
    path("logout/", views.logoutUser, name = "logout"),
    path('population-chart/', views.population_chart, name='population-chart'),


    path("", views.home, name = "home"),
    path("send_message", views.send_email, name = "send_message"),
    path("send_channel_message", views.send_channel_message, name = "send_channel_message"),
]
