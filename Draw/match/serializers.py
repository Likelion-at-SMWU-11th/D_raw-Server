from rest_framework.serializers import ModelSerializer
from .models import MatchUser

class MatchModelSerializer(ModelSerializer):
    class Meta:
        model = MatchUser
        fields = '__all__'