from django.urls import path

from .views import viral_video_detail


urlpatterns = [
    path('<int:pk>/', viral_video_detail,
         name='viral-video-detail'),
]
