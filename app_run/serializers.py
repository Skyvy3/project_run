from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User


class RunSerializer(serializers.ModelSerializer):
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