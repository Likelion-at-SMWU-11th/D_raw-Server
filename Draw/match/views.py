from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import MatchUser
from account.models import Guide
from .forms import MatchBasedForm
from .serializers import GuideModelSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    return render(request, 'check.html')

# 이용자 -> 안내사 빠르게 찾기
class QuickList(APIView):
    def get(self, request):
        # 이용자 장소 갖고 오기
        # 임의로 서울로 지정
        place = '서울특별시 용산구'
        # place = User.objects.get
        location = Guide.objects.get(location__contains = place)
        serializer = GuideModelSerializer(location, many=True)
        return Response(serializer.data)
    # def put(self, request): # 신청정보 수정
    
    # def delete(self, request): # 취소하기

# 이용자 -> 안내사 프로필 보고 찾기
# 위와 동일하되, 성별, 성인, 장소만 추가
class ProfileList(APIView):
    def get(self, request):
        pass

# 프로필 상세보기
class ProfileDetailList(APIView):
    def get_object(self, pk):
        try:
            return Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guide = self.get_object(pk)
        serializer = Guide(guide)

# 안내사 -> 이용자 빠른/제안받은 매칭 보기
def search(request):
    # 빠르게 매칭만
    # if User.objects.choice == quick_choice:
    # 제안받은매칭만
    # else:
    return render(request, 'search.html')
