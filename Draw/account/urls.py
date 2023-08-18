from django.urls import path, include
from . import views
from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *

urlpatterns = [
    #kakao login url
    path('signup/', JWTSignupView.as_view()), # 회원가입
    path('login/', JWTLoginView.as_view()), # 로그인
    path('login/refresh/', TokenRefreshView.as_view()), # 토큰 재발급
    path('account/kakao/accesstoken/<str:auth_code>', KakaoCallBackView.as_view()),
    path('role/', role_select, name='role-select'), #guide인지 user인지 설정
    #guide url
    path('bestguide/', views.BestGuide),
    path('guideprofile/', guide_profile_view, name='guide-profile'),
    path('update_guide_career/', views.update_guide_career, name='update_guide_career'),
    path('create_guide_profile', views.guide_create_form_view, name = 'create-guide'),
    ]