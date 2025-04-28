from django.contrib.auth.models import AbstractUser
from django.db import models

class FitUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)

    # Friends list: Many-to-many with self
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

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
        # You can add more if needed
    ]

    # Multiple selections of fitness interests
    interests = models.JSONField(blank=True, default=list)

    def __str__(self):
        return self.username
