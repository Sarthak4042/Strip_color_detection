from django.urls import path
from . import views

urlpatterns = [
    path('api/analyze/', views.analyze_endpoint, name='analyze_endpoint'),
]
