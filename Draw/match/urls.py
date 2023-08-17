from django.urls import path, include
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.match, name='match'),
    path('check/', views.check, name='check'),
    path('quick/', views.QuickList.as_view(), name='quick'),
    path('profile/', views.ProfileList.as_view, name='profile'),
    path('profile/<int:pk>/', views.ProfileDetailList.as_view())
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)