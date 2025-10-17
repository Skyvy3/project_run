from django.contrib import admin
from django.urls import path, include
from app_run.views import api_endpoint, RunViewSet, Users, StartRunView,StopRunView, AthleteInfoView, ChallengeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api/runs', RunViewSet)
router.register('api/users', Users, basename='users')
challenge_detail = ChallengeViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', api_endpoint),
    path('', include(router.urls)),
    path('api/runs/<int:run_id>/start/', StartRunView.as_view()),
    path('api/runs/<int:run_id>/stop/', StopRunView.as_view()),
    path('api/athlete_info/<int:user_id>/', AthleteInfoView.as_view(), name='athlete-info'),
    path('api/challenges/<int:pk>/', challenge_detail, name='challenge-detail'),

]