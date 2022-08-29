from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('video_feed',views.video_feed, name='video_feed'),
    path('object_feed',views.object_feed, name='object_feed'),
    
    # path('detect_result',views.detect_result, name='detect_result'),
]