from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class FitUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)

    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    friend_requests_sent = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='friend_requests_received',
        blank=True
    )

    # Fitness-related interests
    FITNESS_INTEREST_CHOICES = [
        ('yoga', 'Yoga'),
        ('running', 'Running'),
        ('swimming', 'Swimming'),
        ('weightlifting', 'Weightlifting'),
        ('cycling', 'Cycling'),
        ('crossfit', 'CrossFit'),
        ('pilates', 'Pilates'),
        ('hiking', 'Hiking'),
        ('boxing', 'Boxing'),
        ('martial_arts', 'Martial Arts'),
        ('dance', 'Dance Fitness'),
        ('climbing', 'Rock Climbing'),
        ('rowing', 'Rowing'),
        ('triathlon', 'Triathlon'),
        ('gymnastics', 'Gymnastics'),
        ('powerlifting', 'Powerlifting'),
        ('calisthenics', 'Calisthenics'),
        ('skiing', 'Skiing'),
        ('snowboarding', 'Snowboarding'),
        ('surfing', 'Surfing'),
    ]

    interests = models.JSONField(blank=True, default=list)

    generated_workout = models.JSONField(blank=True, null=True, default=None)

    def __str__(self):
        return self.username
    
    def get_badges(self):
        badges = []

        # Workout-based badges
        workout_count = self.workouts.count()
        if workout_count >= 1:
            badges.append('First Workout')
        if workout_count >= 10:
            badges.append('10 Workouts')
        if workout_count >= 50:
            badges.append('50 Workouts')
        if workout_count >= 100:
            badges.append('100 Workouts')

        # Time-based badges
        account_age = now() - self.date_joined
        if account_age >= timedelta(days=30):
            badges.append('1 Month Member')
        if account_age >= timedelta(days=180):
            badges.append('6 Months Member')
        if account_age >= timedelta(days=365):
            badges.append('1 Year Champion')

        return badges

class Workout(models.Model):
    user = models.ForeignKey(FitUser, on_delete=models.CASCADE, related_name='workouts')
    workout_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout_type} - {self.duration_minutes} min - {self.user.username}"


class WorkoutGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(FitUser, related_name='workout_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()

class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    group = models.ForeignKey(WorkoutGroup, on_delete=models.CASCADE, related_name='challenges')
    start_date = models.DateField()
    end_date = models.DateField()

    winner = models.ForeignKey(FitUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='challenges_won')

    def __str__(self):
        return f"{self.title} ({self.group.name})"

    def is_active(self):
        today = now().date()
        return self.start_date <= today <= self.end_date