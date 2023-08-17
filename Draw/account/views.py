from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from Draw.settings import SOCIAL_OUTH_CONFIG
import requests, json
from .models import User, Guide
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, UserSerializer, BestGuideSerializer
from .forms import GuideCreateForm, GuideProfileEditForm

class JWTSignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입에 성공하였습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            # 쿠키에 넣어주기(set_cookie)
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTLoginView(APIView):
    def post(self, request):
        user = authenticate(
            user_id=request.data.get("user_id"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인에 성공하였습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

"""
인가코드 요청
"""
class KakaoCallBackView(APIView):
    def get(self, request, auth_code):
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
       
        """
        토큰 요청
        """
        token_req = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={auth_code}')
        token_json = token_req.json()
        error = token_json.get('error')
        if error is not None:
            raise json.JSONDecodeError(error)

        access_token = token_json.get('access_token') # access token 추출

        """
        사용자 정보(profile) 요청
        """
        profile_req = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"}
        )
        profile_json = profile_req.json()
        email = profile_json.get("kakao_account").get("email") # email 값
        properties = profile_json.get("kakao_account").get("profile")
        nickname = properties.get("nickname") # 이름값
        profile_photo = properties.get("profile_image_url") # 프로필 사진

        try: # DB에 email이 존재하는지 확인
            user = User.objects.get(email=email)
        except User.DoesNotExist: # DB에 없다면 계정 생성
            user = User.objects.create(
                user_id = email.split(sep='@')[0],
                email = email,
                nickname = nickname,
            )
            user.save()
            if profile_photo is not None: # kakao profile에 image가 있다면
                profile_photo_req = requests.get(profile_photo)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(profile_photo_req.content)
                )
        login(request, user)
        # jwt token 접근
        token = TokenObtainPairSerializer.get_token(user)
        jwt_refresh_token = str(token)
        jwt_access_token = str(token.access_token)
        res = Response(
            {
                "user": nickname,
                "email": email,
                "profile_photo": profile_photo,
                "message": "카카오 로그인에 성공하였습니다.",
                "token": {
                    "access": jwt_access_token,
                    "refresh": jwt_refresh_token,
                },
            },
            status = status.HTTP_200_OK
        )
        res.set_cookie("access", jwt_access_token, httponly=True)
        res.set_cookie("refresh", jwt_refresh_token, httponly=True)
        
        return res

   
'''
# 회원가입 관련 View
def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'index.html', _context)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoLoginLogic(request):
    _restApiKey = 'd8fd6327b24b302b1d20f0690b10d3f4'
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'  
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = 'd8fd6327b24b302b1d20f0690b10d3f4' 
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'loginSuccess.html')

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'loginoutSuccess.html')
    else:
        return render(request, 'logoutError.html')

class KakaoSignInCallBackView(View):
    def get (self, request):
        auth_code = request. GET. get ( 'code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization code',
            'client id' :'d8fd6327b24b302b1d20f0690b10d3f4',
            'redirection_uri': 'http://localhost:8000/users/signin/kakao/callback',
            'code': auth_code,
        }
        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        user_info_response = request.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization":f'Bearer ${access_token}'})

        return JsonResponse({"user_info": user_info_response.json()})

def methodsCheck(request, id):
    if(request.method == 'GET'):
        print(f"GET QS : {request.GET.get('data', '')}")
        print(f"GET Dynamic Path : {id}")
    
    # PostMan으로 Localhost 테스트를 위해 CSRF 해제
    # project/settings.py 파일에서 
    # MIDDLEWARE -> 'django.middleware.csrf.CsrfViewMiddleware' 주석 처리
    elif(request.method == 'POST'):
        print(f"POST QS : {request.GET.get('data', '')}")
        print(f"POST Dynamic Path : {id}")
        return HttpResponse("POST Request.", content_type="text/plain")
    return render(request, 'methodGet.html')
'''

## 안내사 관련 View
#우수 안내사 View
def BestGuide(request):
    bestguidelist = Guide.objects.all().order_by('rate')
    serializer_class = BestGuideSerializer
    context = {
        'bestguidelist' : bestguidelist
    }
    return render(request, 'BestGuide.html', context)

# 안내사 프로필 생성 View
def guide_create_form_view(request):
    if request.method == 'GET':
        form = GuideCreateForm()
        context = {'form' : form}
        return render(request, 'GuideCreate.html', context)
    
    else:
        form = GuideCreateForm(request.POST)

        if form.is_valid():
            guide = form.save(commit=False)
            guide.rate = int(form.cleaned_data['rate'])  # 입력된 rate 데이터를 숫자로 변환하여 할당
            guide.save()
            return render(request, 'GuideProfile.html')
        else:
            return render(request, 'GuideCreate.html')

# 안내사 활동지역 View
def guide_location_form_view(request):
    if request.method == 'GET':
        form = GuideCreateForm()
        context = {'form' : form}
        return render(request, 'GuideLocation.html', context)
    
    else:
        form = GuideCreateForm(request.POST)

        if form.is_valid():
            guide = form.save(commit=False)
            guide.rate = int(form.cleaned_data['rate'])  # 입력된 rate 데이터를 숫자로 변환하여 할당
            guide.save()
            return render(request, 'index.html')
        else:
            return render(request, 'GuideLocation.html')

# 안내사 프로필 보여주기 View
def guide_profile_view(request):
        return render(request, 'GuideProfile.html')

# 안내사 프로필 수정 View
def guide_profile_edit_view(request, guide_id):
    guide = Guide.objects.get(pk=guide_id)

    if request.method == 'POST':
        form = GuideProfileEditForm(request.POST)
        if form.is_valid():
            guide.start_date = form.cleaned_data['start_date']
            guide.career = form.cleaned_data['career']
            guide.save()
            return redirect('guide_profile', guide_id=guide.id)  # Redirect to the guide profile page
    else:
        form = GuideProfileEditForm(initial={'start_date': guide.start_date, 'career': guide.career})

    context = {
        'form': form,
        'guide': guide,
    }

    return render(request, 'guide_profile_edit.html', context)
