from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User


class AthleteSerializer(serializers.ModelSerializer):
    athlete_data = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'athlete_data']




class RunSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer()
    class Meta:
        model = Run
        fields = ['id','athlete', 'comment', 'created_at']





class UsersSerializers(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()#Вычисляю поле type
    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'