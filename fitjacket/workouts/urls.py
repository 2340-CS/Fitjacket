from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='workouts.dashboard'),
    path('log_workout', views.log_workout, name = 'workouts.log_workout'),
    path('log_fitness', views.log_fitness, name = 'workouts.log_fitness'),
    path('workoutHistory', views.workoutHistory, name = 'workouts.workoutHistory'),
    
]