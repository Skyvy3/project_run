
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Run, AthleteInfo, Challenge
from rest_framework import viewsets, status
from app_run.serializers import RunSerializer,UsersSerializers, AthleteInfoSerializer, ChallengeSerializer

#Самый простой Апи эндпоинт который отдает JSON
@api_view(['GET'])
def api_endpoint(request):
    context = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(context)


#Пагинация
class RunsUsersPagination(PageNumberPagination):
    page_size = 10  # значение по умолчанию, если не указан size
    page_size_query_param = 'size'  # ← параметр для изменения размера страницы
    max_page_size = 50
    page_query_param = 'page'



class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_filter = ['created_at']
    pagination_class = RunsUsersPagination

    def paginate_queryset(self, queryset):
        # Применяем пагинацию ТОЛЬКО если передан параметр 'size'
        if self.request.query_params.get('size') is not None:
            return super().paginate_queryset(queryset)
        # Иначе — отключаем пагинацию
        return None

class Users(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializers

    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = RunsUsersPagination


    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False).annotate(
            runs_finished_count=Count('runs', filter=Q(runs__status='finished'))
        )

        user_type = self.request.query_params.get('type')

        if user_type == 'coach':
            queryset = queryset.filter(is_staff=True)
        elif user_type == 'athlete':
            queryset = queryset.filter(is_staff=False)

        return queryset

    def paginate_queryset(self, queryset):
        # Применяем пагинацию ТОЛЬКО если передан параметр 'size'
        if self.request.query_params.get('size') is not None:
            return super().paginate_queryset(queryset)
        # Иначе — отключаем пагинацию
        return None


class StartRunView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'init':
            return Response(
                {'error': 'Run has already been started or finished.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = 'in_progress'
        run.save(update_fields=['status'])

        return Response({
            'message': 'Run started',
            'run_id': run.id,
            'status': run.status
        })

class StopRunView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'in_progress':
            return Response(
                {'error': 'Run is not in progress.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        run.status = 'finished'
        run.save(update_fields=['status'])

        # === НОВАЯ ЛОГИКА: проверка на 10 завершённых забегов ===
        finished_runs_count = Run.objects.filter(
            athlete=run.athlete,
            status='finished'
        ).count()

        if finished_runs_count >= 10:
            Challenge.objects.get_or_create(
                athlete=run.athlete,
                full_name="Сделай 10 Забегов!"
            )
        # ======================================================

        return Response({
            'message': 'Run stopped',
            'run_id': run.id,
            'status': run.status
        })

class ChallengeViewSet(ReadOnlyModelViewSet):
    queryset = Challenge.objects.select_related('athlete').all()
    serializer_class = ChallengeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athlete']





class AthleteInfoView(APIView):
    def get_athlete_info(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        athlete_info, created = AthleteInfo.objects.get_or_create(user=user)
        return athlete_info

    def get(self, request, user_id):
        athlete_info = self.get_athlete_info(user_id)
        serializer = AthleteInfoSerializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, user_id):
        athlete_info = self.get_athlete_info(user_id)
        serializer = AthleteInfoSerializer(athlete_info, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)