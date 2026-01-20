# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', views.survey, name='survey'),
    path('recommend/', views.recommend, name='recommend'),
    

]