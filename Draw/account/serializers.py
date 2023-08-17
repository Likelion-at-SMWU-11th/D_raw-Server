from .models import User, Guide
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data): # 회원가입
        user_id = validated_data.get('user_id')
        password = validated_data.get('password')
        email = validated_data.get('email')
        nickname = validated_data.get('nickname')
        introduce = validated_data.get('introduce')
        profile_photo = validated_data.get('profile_photo')
        gender = validated_data.get('gender')
        user = User(
            user_id = user_id,
            email = email,
            nickname = nickname,
            introduce = introduce,
            profile_photo = profile_photo,
            gender = gender,
        )
        user.set_password(password)
        user.save()
        return user

class GuideCreateSerializer(SignupSerializer):
    class Meta:
        model = Guide
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BestGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide 
        fields = ['rate']