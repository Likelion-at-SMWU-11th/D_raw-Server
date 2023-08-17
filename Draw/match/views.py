from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import QuerySet

from .models import MatchUser
from account.models import User, Guide
from .forms import MatchBasedForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.serializers import SignupSerializer

# 이용자 정보 저장
@login_required
def match(request):
    if request.method == "POST":
        form = MatchBasedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('check.html')
    else:
        form = MatchBasedForm()
    return render(request, 'match.html', {'form' : form})

# 매칭 방법 선택
def check(request):
    # 빠르게 찾기
    if MatchUser.objects.get(method='quick'):
        choice = '빠르게 찾기'
    # 프로필 보고 찾기
    else:
        choice = '프로필 보고 찾기'
    return render(request, 'check.html', { 'choice':choice })

# 이용자 -> 안내사 빠르게 찾기
class QuickList(APIView):
    def get_object(self, pk):
        return get_object_or_404(Guide, pk=pk)
    
    def get(self, request):
        # 이용자 장소 갖고 오기 -> 임의로 서울로 지정
        place = '서울특별시 용산구'
        # place = User.objects.get(place=place)
        location = Guide.objects.get(location__contains = place)
        serializer = SignupSerializer(location, many=True)
        return Response(serializer.data)
    
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
    if MatchUser.objects.get(method='quick'):
        choice = '빠르게 찾기'
    # 프로필 보고 찾기
    else:
        choice = '프로필 보고 찾기'
    return render(request, 'search.html', { 'choice':choice })

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