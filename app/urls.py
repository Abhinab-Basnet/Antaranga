from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', views.survey, name='survey'),
    path('recommend/', views.recommend, name='recommend'),
    
    # NEW: This captures the clicked place name from result.html
    path('destination/<slug:place_slug>/', views.destination_detail, name='detail'),
]