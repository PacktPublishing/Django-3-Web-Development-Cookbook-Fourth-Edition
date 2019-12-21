from django.urls import path

from .views import viral_video_detail

app_name = "viral_videos"


urlpatterns = [
    path('<int:pk>/', viral_video_detail,
         name='viral-video-detail'),
]
