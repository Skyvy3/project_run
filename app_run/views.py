from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response



#Самый простой Апи эндпоинт который отдает JSON
@api_view(['GET'])
def api_endpoint(request):
    context = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(context)