from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "workouts"

urlpatterns = [
    path('generate/', views.workout_plan_form, name='workout_plan_form'),
    path('results/', views.workout_plan_results, name='workout_plan_results'),
]