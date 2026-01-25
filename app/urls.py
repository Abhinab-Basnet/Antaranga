from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', views.survey, name='survey'),
    path('recommend/', views.recommend, name='recommend'),
    
    # FIX: Add the logout path so the template can find it
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # FIX: Add the destination detail path for the "Big Orange" page
    path('destination/<slug:destination_slug>/', views.detail, name='detail'),
]