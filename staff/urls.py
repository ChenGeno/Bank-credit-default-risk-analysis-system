from django.urls import path
from . import views

app_name = 'bc_gate'
urlpatterns = [
    path("homepage/", views.homepage),
    path("index/", views.index),
    path("login/", views.user_login),
    path("mq/", views.model_query),
    path("register/", views.user_register),
    path("basic_info/", views.basic_info),
    path('application_info/', views.application_info),
    path('personal_info/', views.personal_info),
    path('step_info/', views.step_info, name='step_info'),
    path('user_tour/', views.user_tour),
    path('check_result/', views.check_result),
    path('landing/', views.landing),
    path('dashboard/', views.dashboard, name='dashboard'),

    path("logout/", views.logout, name='logout'),
    path("bind_member/", views.bind_member, name='bind_member'),
    path("apply_loan/", views.apply_loan, name='apply_loan'),
]