from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.match, name='match'),
    path('check/', views.check, name='check'),
    path('quick/', views.QuickList.as_view(), name='quick'),
    path('profile/', views.ProfileList.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileDetailList.as_view()),
    path('mypage/user', views.GuideList, name='mypage-user'),
    path('mypage/guide', views.UserList, name='mypage-guide'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)