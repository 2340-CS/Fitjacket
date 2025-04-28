from django.urls import path
from . import views
from .views import logs_view, leaderboard_view

app_name = "workoutlogs"

urlpatterns = [
    path('logs', logs_view, name="logs"), 
    path('leaderboard', leaderboard_view, name='leaderboard')
]