from django.contrib import admin
from django.urls import path, include

from account import urls as account_url
from main import urls as main_url
from match import urls as match_url
from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account_url)),
    #kakao 계정 관련
    path('account/', include('allauth.urls')),
    path('', views.index, name='kakao'),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),
 
    # GET | POST - Methods / Params | QueryString
    path('methodsCheck/<int:id>', views.methodsCheck),

    #매칭 관련
    path('main/', include(main_url)),
    path('match/', include(match_url)),



]
