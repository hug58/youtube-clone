from django.urls import path
from .views import create_video, video_detail, like_video, dislike_video, popular_videos

app_name = 'content'

urlpatterns = [
    path('create/', create_video, name='create_video'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('video/<int:video_id>/like/', like_video, name='like_video'),
    path('video/<int:video_id>/dislike/', dislike_video, name='dislike_video'),
    path('popular/', popular_videos, name='popular_videos'),
]


