from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('kakao/login/',views.KakaoSignup.as_view(), name = 'signup'),
]