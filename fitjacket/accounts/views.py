from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomErrorList
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

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class = CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home')
        


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('accounts.login')


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
            
            # Store in session to display on results page
            request.session['generated_plan'] = plan
            return redirect('workout_plan_results')
    else:
        form = WorkoutPlanForm()
    
    return render(request, 'workout/generate_plan.html', {'form': form})

def workout_plan_results(request):
    plan = request.session.get('generated_plan', None)
    if not plan:
        return redirect('workout_plan_form')
    
    return render(request, 'workout/plan_results.html', {'plan': plan})

@method_decorator(csrf_exempt, name='dispatch')
class WorkoutPlanAPI(View):
    def post(self, request):
        data = json.loads(request.body)
        assistant = WorkoutAIAssistant()
            
        plan = assistant.generate_workout_plan(
            goals=data.get('goals', 'general_fitness'),
            activity_level=data.get('activity_level', 'beginner'),
            available_equipment=data.get('available_equipment', ['bodyweight']),
            days_per_week=data.get('days_per_week', 3),
            preferences=data.get('preferences'),
            duration_weeks=data.get('duration_weeks', 4)
        )
            
        return JsonResponse(plan)