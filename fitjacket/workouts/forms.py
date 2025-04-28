from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe


class WorkoutPlanForm(forms.Form):
    GOAL_CHOICES = [
        ('build_muscle', 'Build Muscle'),
        ('lose_weight', 'Lose Weight'),
        ('improve_endurance', 'Improve Endurance'),
        ('general_fitness', 'General Fitness'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    goals = forms.ChoiceField(choices=GOAL_CHOICES)
    activity_level = forms.ChoiceField(choices=LEVEL_CHOICES)

    days_per_week = forms.IntegerField(
        min_value=1,
        max_value=7,
        initial=3,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )