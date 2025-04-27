from django.contrib import admin
from .models import FitnessData, Workout

# Register your models here.

class WorkoutAdmin(admin.ModelAdmin):
    ordering = ['user']
    search_fields = ['user']

admin.site.register(FitnessData, WorkoutAdmin)
admin.site.register(Workout)