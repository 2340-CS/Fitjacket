from django.shortcuts import render, redirect
from .models import Workout, FitnessData
from datetime import datetime

# Create your views here.

def dashboard(request):
    if (FitnessData.objects.filter(user=request.user).first() is None):
        fitness = FitnessData()
        fitness.user = request.user
        fitness.date = datetime.today()
        fitness.steps = 0
        fitness.miles = 0
        fitness.flights_climbed = 0
        fitness.restingHR = 0
        fitness.save()
        
    # super().get_query_set().filter(author=self.request.user)
    currentData = FitnessData.objects.filter(user=request.user).first()
    
    # currentData = Fitness
    data = {}
    data['steps'] = currentData.steps
    data['miles'] = currentData.miles
    data['stairs'] = currentData.flights_climbed
    data['rHR'] = currentData.restingHR
    data['history'] = FitnessData.objects.values_list('miles', flat = True)


    
    return render(request, 'workouts/dashboard.html', {'data': data})


def workoutHistory(request):
    data = {}
    data['workouts'] = Workout.objects.order_by('-user_id').all()
    data['fitness'] = FitnessData.objects.order_by('-user_id').all()
    return render(request, 'workouts/history.html', {'data':data})


def log_fitness(request):
    if request.method == 'POST' and request.POST['steps'] != '' and request.POST['miles'] != '' and request.POST['flights'] != '' and request.POST['hr'] != '':
        fitness = FitnessData()
        fitness.user = request.user
        fitness.date = datetime.today()
        fitness.steps = request.POST['steps']
        fitness.miles = request.POST['miles']
        fitness.flights_climbed = request.POST['flights']
        fitness.restingHR = request.POST['hr']
        fitness.save()
        # return redirect('dashboard.html')
    return redirect('workouts.dashboard')


def log_workout(request):
    if request.method == 'POST' and request.POST['workout']!= '' and request.POST['intensity'] != '':
        workout = Workout()
        workout.user = request.user
        workout.date = datetime.today()
        workout.workout = request.POST['workout']
        workout.intensity = request.POST['intensity']
        if request.POST['reps'] != '':
            workout.reps = request.POST['reps']
        workout.save()
    return redirect('workouts.dashboard')
