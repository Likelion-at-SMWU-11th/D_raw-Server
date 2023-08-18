from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import QuerySet

from .models import MatchUser
from account.models import User, Guide
# from .forms import MatchBasedForm, Choice

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.serializers import SignupSerializer
import requests

# 이용자 정보 저장
@login_required
def match(request):
    if request.method == "POST" and request.user.role == 'User':
        start_time = request.POST.get('start_time')
        time_choice = request.POST.get('time_choice')
        start_hour = request.POST.get('start_hour')
        place = request.POST.get('place')
        blind = request.POST.get('blind')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        prefer_gender = request.POST.get('prefer_gender')
        list = request.POST.get('list')
        plus = request.POST.get('plus')
        care = request.POST.get('care')

        user = request.user
        user.start_time = start_time
        user.time_choice = time_choice
        user.start_hour = start_hour
        user.place = place 
        user.blind = blind
        user.birth = birth
        user.gender = gender
        user.prefer_gender = prefer_gender
        user.list = list
        user.plus = plus
        user.care = care
        user.save()
        return render(request, 'match.html', {'user' : user})
    else: 
        pass

# 매칭 방법 선택
@login_required
def check(request):
    if request.method == "GET" and request.user.role == 'User':
        method = request.GET.get('check')
        user = request.user

        if method == '빠르게 찾기':
            user.method = method
            user.save()
            return render(request, 'quick.html', {'user' : user})
        else:
            user.method = method
            user.save()
            return render(request, 'profile.html', {'user' : user})
    return render(request, 'check.html')

# 이용자 -> 안내사 빠르게 찾기
class QuickList(APIView):
    def get_object(self, pk):
        return get_object_or_404(Guide, pk=pk)
    
    def get(self, request): # 정보 가져오기
        user = request.user
        user_place = user.place

        filtered_place = Guide.objects.filter(location__contains=user_place)
        serializer = SignupSerializer(filtered_place, many=True)
        return Response(serializer.data)

    def put(self, request, pk): # 신청정보 수정
        user = request.user
        guide = get_object_or_404(Guide, pk=pk, user=user)

        serializer = SignupSerializer(guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk): # 취소하기
        # 로그인한 정보 가져오기
        user = request.user

        # Guide모델에서 해당 사용자의 정보 가져오기
        guide = self.get_object(pk=pk, user=user)
        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 이용자 -> 안내사 프로필 보고 찾기
class ProfileList(APIView):
    # 필터링
    def get(self, request):
        gender = request.GET.get('gender')
        adult = request.GET.get('adult')
        career = request.GET.get('career')

        filters = QuerySet()
        if gender == '여성':
            Guide.objects.filter(gender='여성')
        else:
            Guide.objects.filter(gender='남성')

        if adult == '성인':
            # Guide.objects.filter(age >'20')
            filters &= QuerySet(age__gt=20)
        else:
            Guide.objects.all()

        if career ==  '1년 이상':
            Guide.objects.filter(career=1)
        elif career == '2년 이상':
            Guide.objects.filter(career=2)
        elif career == '3년 이상':
            Guide.objects.filter(career=3)
        else: # 상관없음
            Guide.objects.all()

    def put(self, request, pk): # 신청정보 수정
        guide = self.get_object(pk)
        serializer = SignupSerializer(guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk): # 취소하기
        guide = self.get_object(pk)
        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 프로필 상세보기
class ProfileDetailList(APIView):
    def get_object(self, pk):
        try:
            return Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guide = self.get_object(pk)
        serializer = SignupSerializer(guide)
        return Response(serializer.data)

# 안내사 -> 이용자 빠른/제안받은 매칭 보기
def search(request):
    # 빠르게 매칭만
    if request.user.role == 'Guide':
        user = User.objects.filter(method='quick')
    # 프로필 보고 찾기
    else:
        user = User.objects.filter(method='profile')
    return render(request, 'search.html', {'user':user })

# 내 매칭-이용자가 보는 화면
class GuideList(APIView):
    def get(self, request, pk):
        guide = self.get_object(pk)
        serializer = SignupSerializer(guide)
        return Response(serializer.data)

# 내 매칭-안내사가 보는 화면
class UserList(APIView):
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = SignupSerializer(user)
        return Response(serializer.data)