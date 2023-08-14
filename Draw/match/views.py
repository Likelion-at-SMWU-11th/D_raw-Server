from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import MatchUser
from .forms import MatchBasedForm

from rest_framework import viewsets
from account.models import Guide, GuideLocation

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

def check(request):
    quick_choice = request.GET.get('quick')
    profile_choice = request.GET.get('profile')

    # 선택지 저장
    if quick_choice:
        # User.objects.filter(userId=user).update(choice=quick_choice) 빠른 매칭으로 회원정보 저장
        pass
    elif profile_choice:
         # User.objects.filter(userId=user).update(choice=profile_choice) 프로필 보기 매칭으로 회원정보 저장
        pass

    return render(request, 'check.html')
    # return render(request, 'check.html', {'user'} : user)


# def quick(request): # 정보 수정하기, 취소하기 기능
#     return render(request, 'quick.html')

class ProfileList(viewsets.ModelViewSet):
    
    

# def profile(request): # 필터링 (성별, 성인, 봉사경력)
#     # User.objects.filter(userId=user).values()
#     return render(request, 'profile.html')

def search(request):
    # 빠르게 매칭만
    # if User.objects.choice == quick_choice:
    # 프로필 보기 매칭만
    # else:
    return render(request, 'search.html')
