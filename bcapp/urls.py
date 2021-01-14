from django.urls import path
from . import views

urlpatterns = [
    path("homepage/", views.homepage),
    path("index/", views.index),
    path("login/", views.login),
    path("mq", views.model_query()),
]