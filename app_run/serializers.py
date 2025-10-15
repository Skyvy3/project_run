from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User




class AthleteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteDataSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = ['id', 'athlete', 'comment', 'created_at', 'athlete_data', 'status']




class UsersSerializers(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()#Вычисляю поле type
    runs_finished = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'

    def get_runs_finished(self, obj):
        # obj — это User
        return obj.runs.filter(status='finished').count()