import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from accounts.models import Workout
from django.conf import settings
from django.db.models import Sum
from accounts.models import FitUser

@login_required
def logs_view(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_manual':
            workout_type = request.POST.get('workout_type')
            duration_minutes = request.POST.get('duration_minutes')
            calories_burned = request.POST.get('calories_burned')

            if workout_type and duration_minutes and calories_burned:
                Workout.objects.create(
                    user=user,
                    workout_type=workout_type,
                    duration_minutes=int(duration_minutes),
                    calories_burned=int(calories_burned)
                )

        elif action == 'import_strava':
            strava_workout_id = request.POST.get('strava_workout_id')

            if strava_workout_id:
                access_token = settings.STRAVA_API_KEY

                url = f"https://www.strava.com/api/v3/activities/{strava_workout_id}"
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    workout_type = data.get('name', 'Strava Workout')
                    elapsed_time = data.get('elapsed_time', 0)
                    calories = data.get('kilojoules', 0)

                    Workout.objects.create(
                        user=user,
                        workout_type=workout_type,
                        duration_minutes=elapsed_time // 60,
                        calories_burned=int(calories) if calories else 0
                    )

                else:
                    print(f"Failed to import from Strava: {response.status_code} - {response.text}")

        return redirect('workoutlogs:logs')

    # Query workouts normally
    workouts = user.workouts.all().order_by('-date')

    # Prepare JSON version for Chart.js
    workouts_json = json.dumps(
        list(workouts.values('date', 'workout_type', 'duration_minutes', 'calories_burned')),
        cls=DjangoJSONEncoder
    )

    return render(request, 'workoutlogs/logs.html', {
        'workouts': workouts,
        'workouts_json': workouts_json,
    })

@login_required
def leaderboard_view(request):
    users = FitUser.objects.all()
    leaderboard_users = []

    for user in users:
        total_minutes = user.workouts.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        calories_burned = user.workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        badges = user.get_badges()  
        badge_count = len(badges)  

        score = (total_minutes * 1) + (calories_burned * 0.5) + (badge_count * 20)

        leaderboard_users.append({
            'username': user.username,
            'total_minutes': total_minutes,
            'calories_burned': calories_burned,
            'badge_count': badge_count,  
            'score': int(score),
        })

    leaderboard_users = sorted(leaderboard_users, key=lambda x: x['score'], reverse=True)

    return render(request, 'workoutlogs/leaderboard.html', {'leaderboard_users': leaderboard_users})
