from django.urls import path

from .views import ViralVideoList, viral_video_detail

app_name = "viral_videos"


urlpatterns = [
    path("", ViralVideoList.as_view(), name="viral_video_list"),
    path("<uuid:pk>/", viral_video_detail, name="viral_video_detail"),
]
