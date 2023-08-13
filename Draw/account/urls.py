from django.urls import path, include
from . import views
from django.urls import path

urlpatterns = [
    path('logout/', views.index),
    path('guidecreate/', views.guide_create_form_view),
    path('bestguide/', views.BestGuide),
    path('guidelocation/', views.guide_location_form_view),
]