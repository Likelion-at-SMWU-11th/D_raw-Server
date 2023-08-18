from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from Draw.settings import SOCIAL_OUTH_CONFIG
import requests, json
from .models import User, Guide
from .serializers import SignupSerializer, UserSerializer, BestGuideSerializer
from .forms import GuideCreateForm, GuideProfileEditForm
from django.http import JsonResponse
from .serializers import SignupSerializer, UserSerializer

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
            username=request.data.get("username"), password=request.data.get("password")
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
        profile_photo = properties.get("profile_image_url") # 프로필 사진
        username = profile_json.get("kakao_account").get("username") #사용자 이름

        try: # DB에 email이 존재하는지 확인
            user = User.objects.get(email=email)
        except User.DoesNotExist: # DB에 없다면 계정 생성
            user = User.objects.create(
                username = email.split(sep='@')[0],
                email = email,
            )
            user.save()
            if profile_photo is not None: # kakao profile에 image가 있다면
                profile_photo_req = requests.get(profile_photo)
                user.avatar.save(
                    f"{username}-avatar", ContentFile(profile_photo_req.content)
                )
        login(request, user)
        # jwt token 접근
        token = TokenObtainPairSerializer.get_token(user)
        jwt_refresh_token = str(token)
        jwt_access_token = str(token.access_token)
        res = Response(
            {
                "user": username,
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
## 안내사 관련 View
#우수 안내사 View
def BestGuide(request):
    bestguidelist = Guide.objects.all().order_by('rate')
    serializer = BestGuideSerializer()
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
            return redirect('guideprofile/', guide_id=guide.id)  # Redirect to the guide profile page
    else:
        form = GuideProfileEditForm(initial={'start_date': guide.start_date, 'career': guide.career})

    context = {
        'form': form,
        'guide': guide,
    }

    return render(request, 'guide_profile_edit.html', context)


# 회원가입 후 회원 구분
def account_create_view(request):
    if request.method == 'GET': # 디지털 약자입니다 선택할 경우
        return render(request, '')

    elif request.method == 'POST': # 안내사입니다 선택할 경우
        form = GuideCreateForm()
        context = {'form' : form}
        return render(request, 'GuideCreate.html', context)
    
    else:
        form = GuideCreateForm(request.POST)

        if form.is_valid():
            guide = form.save(commit=False)
            guide.save()
            return render(request, 'GuideProfile.html')
        else:
            return render(request, 'GuideCreate.html')