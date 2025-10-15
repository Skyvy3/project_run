from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Run
from rest_framework import viewsets
from app_run.serializers import RunSerializer

#Самый простой Апи эндпоинт который отдает JSON
@api_view(['GET'])
def api_endpoint(request):
    context = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(context)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer