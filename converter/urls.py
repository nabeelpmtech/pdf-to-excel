from django.urls import path
from . import views
from .views import upload_view, convert_pdf

app_name = 'converter'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('result/', convert_pdf, name='result'),
]
