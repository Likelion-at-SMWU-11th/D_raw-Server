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
from .models import User, Guide, UserManager
from .serializers import SignupSerializer, UserSerializer, BestGuideSerializer
from .forms import GuideCreateForm, GuideProfileEditForm, UserTypeForm, GuideCareerForm, GuideProfileCreationForm
from django.http import JsonResponse
from .serializers import SignupSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        gender = profile_json.get("kakao_account").get("gender") #성별

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
                "gender": gender,
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
        
        #return res
        return redirect('role-select', auth_code=auth_code)

## 안내사 관련 View
@login_required
def role_select(request):
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            new_role = form.cleaned_data['user_type']
            if new_role in [choice[0] for choice in User.ROLE_CHOICES]:
                user = request.user
                user.role = new_role
                user.save()
                messages.success(request, 'User role has been updated successfully.')
                return redirect('create-guide')
            
    else:
        form = UserTypeForm()
    return render(request, 'user_type_selection.html', {'form':form})
            
#우수 안내사 View
def BestGuide(request):
    bestguidelist = User.objects.filter(role='Guide').order_by('rate')
    serializer = BestGuideSerializer()
    context = {
        'bestguidelist' : bestguidelist
    }
    return render(request, 'BestGuide.html', context)

# guide profile edit view
def update_guide_career(request):
    user = request.user
    if request.method == 'POST':
        form = GuideCareerForm(request.POST)
        if form.is_valid() and user.role == 'guide':
            new_career = form.cleaned_data['career_type']
            user.career = new_career
            user.save()
            messages.success(request, 'User career has been updated successfully.')
            return redirect('guide-profile')  # 수정 완료 후 프로필 페이지로 이동하거나 다른 페이지로 리디렉션
    else:
        form = GuideCareerForm(initial={'career_type': user.career})
    context = {'form': form, 'user': request.user}

    return render(request, 'update_guide_career.html', context)


# 안내사 프로필 생성 View
def guide_create_form_view(request):
    user = request.user
    if request.method == 'GET' and request.user.role == 'Guide':
        form = GuideProfileCreationForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.gender = form.cleaned_data['gender']
            user.age = form.cleaned_data['age']
            user.location = form.cleaned_data['location']
            user.save()
            messages.success(request, 'Guide profile has been updated successfully.')
            return redirect('home')
    else:
        form = GuideProfileCreationForm()

    return render(request, 'create_guide_profile.html', {'form':form})


# 안내사 프로필 보여주기 View
def guide_profile_view(request):
        return render(request, 'GuideProfile.html')

