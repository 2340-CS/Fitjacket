from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import WorkoutPlanForm
from .ai_assistants import WorkoutAIAssistant
import json

@login_required
def workout_plan_form(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            assistant = WorkoutAIAssistant()
            plan = assistant.generate_workout_plan(
                goals=form.cleaned_data['goals'],
                activity_level=form.cleaned_data['activity_level'],
                days_per_week=form.cleaned_data['days_per_week'],
            )

            request.session['workout_plan'] = plan
            return redirect('workouts:workout_plan_results')  # Fixed: namespace:view_name
    else:
        form = WorkoutPlanForm()
    
    return render(request, 'workouts/generate.html', {'form': form})

@login_required
def workout_plan_results(request):
    plan = request.session.get('workout_plan', None)
    if not plan:
        return redirect('workouts:workout_plan_results')  # Fixed: namespace:view_name
    
    return render(request, 'workouts/results.html', {'plan': plan})
