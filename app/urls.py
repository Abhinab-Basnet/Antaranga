from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', views.survey, name='survey'),
    path('recommend/', views.recommend, name='recommend'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reset-survey/', views.reset_survey, name='reset_survey'),
    path('results/', views.results, name='results'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('messenger/', views.messenger, name='messenger'),
    path('messenger/<str:username>/', views.messenger, name='messenger_with_user'),
    path('destination/<slug:destination_slug>/', views.detail, name='detail'),
]   