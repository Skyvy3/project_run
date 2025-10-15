from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_endpoint(request):
    context = settings.MY_SITE
    return Response({'context': context})