from django.contrib import admin
from accounts.models import *

# Register your models here.
admin.site.register(FitUser)
admin.site.register(Workout)
admin.site.register(WorkoutGroup)
admin.site.register(Challenge)