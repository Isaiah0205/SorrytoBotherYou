from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name = "login"),
    path("register/", views.registerPage, name = "register"),
    path("logout/", views.logoutUser, name = "logout"),
    path("", views.home, name = "home"),
    path("send_message", views.send_email, name = "send_message"),
    path("Stats", views.population_chart, name = "Stats"),
]
