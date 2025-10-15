
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app_run import views
from app_run.views import api_endpoint




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', api_endpoint)
]