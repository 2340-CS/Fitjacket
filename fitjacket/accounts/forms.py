from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

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