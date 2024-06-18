from django.urls import path
from .views import (
    JobCreateAPIView,
    ApplicationCreateAPIView,
    JobUpdateAPIView,
    JobListAPIView,
    ApplicationListAPIView,
    JobDeleteAPIView,
    ApplicationDetailsAPIView,
)

urlpatterns = [
    path('jobs/create/', JobCreateAPIView.as_view(), name='job-create'),
    path('applications/create/', ApplicationCreateAPIView.as_view(), name='application-create'),
    path('jobs/<int:pk>/update/', JobUpdateAPIView.as_view(), name='job-update'),
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('applications/', ApplicationListAPIView.as_view(), name='application-list'),
    path('jobs/<int:pk>/delete/', JobDeleteAPIView.as_view(), name='job-delete'),
    path('applications/<int:pk>/', ApplicationDetailsAPIView.as_view(), name='application-details'),
]
