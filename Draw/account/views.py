from django.shortcuts import render, redirect
from django.views import View
import os

def account(request):
    return render(request, 'templates/signup.html')

'''
class KakaoSignupView(View):
    def get(self, request):
        kakao_api = os.environ.get("KAKAO_REST_API_KEY")
        redirect_url = "http://127.0.0.1:8000/account/kakao/login/callback"
        client_id = d8fd6327b24b302b1d20f0690b10d3f4

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_url={redirect_url}")
        '''

 