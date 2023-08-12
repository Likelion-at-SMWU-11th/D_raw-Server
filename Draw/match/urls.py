from django.urls import path
from . import views
urlpatterns = [
    path('', views.match, name='match'),
    path('check/', views.check, name='check'),
    path('quick/', views.quick, name='quick'),
    path('profile/', views.profile, name='profile'),
]
