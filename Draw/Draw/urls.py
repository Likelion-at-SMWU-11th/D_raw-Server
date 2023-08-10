from django.contrib import admin
from django.urls import path, include

from account import urls as account_url
from main import urls as main_url
from match import urls as match_url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('account/', include('allauth.urls')),
    path('main/', include(main_url)),
    path('match/', include(match_url)),
]