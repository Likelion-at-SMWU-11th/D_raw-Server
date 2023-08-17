from rest_framework.serializers import ModelSerializer
from account.models import Guide

class GuideModelSerializer(ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'