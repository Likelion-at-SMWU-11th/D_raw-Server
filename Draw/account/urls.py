from django.urls import path, include
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.index)
]