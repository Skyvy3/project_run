from email.policy import default

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from urllib3 import request

from .models import Run
from rest_framework import viewsets, status
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

    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False)

        user_type = self.request.query_params.get('type')

        if user_type == 'coach':
            queryset = queryset.filter(is_staff=True)
        elif user_type == 'athlete':
            queryset = queryset.filter(is_staff=False)

        return queryset


class StartRunView(APIView):

    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != Run.Status.INIT:
            return Response(
                {'error': 'Run has already been started or finished.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = Run.Status.IN_PROGRESS
        run.save(update_fields=['status'])

        return Response({
            'message': 'Run started successfully',
            'run_id': run.id,
            'status': run.status
        }, status=status.HTTP_200_OK)


class StopRunView(APIView):

    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != Run.status.IN_PROGRESS:
            return Response(
                {'error': 'Run is not in progress. Cannot stop.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = Run.status.FINISHED
        run.save(update_fields=['status'])

        return Response({
            'message': 'Run stopped successfully',
            'run_id': run.id,
            'status': run.status
        }, status=status.HTTP_200_OK)