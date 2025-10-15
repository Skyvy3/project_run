from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from urllib3 import request
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Run
from rest_framework import viewsets
from app_run.serializers import RunSerializer,UsersSerializers

#Самый простой Апи эндпоинт который отдает JSON
@api_view(['GET'])
def api_endpoint(request):
    context = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(context)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

#

class Users(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializers
    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False)

        user_type = self.request.query_params.get('type')

        if user_type == 'coach':
            queryset = queryset.filter(is_staff=True)
        elif user_type == 'athlete':
            queryset = queryset.filter(is_staff=False)

        return queryset