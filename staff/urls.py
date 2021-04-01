from django.urls import path
from . import views

app_name = 'bc_gate'
urlpatterns = [
    path("homepage/", views.homepage),
    path("index/", views.index),
    path("login/", views.login),
    path("logout/", views.logout, name='logout'),
    path("mq/", views.model_query),
    path("register/", views.register),

]