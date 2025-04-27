from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class FitnessData(models.Model):
    date = datetime.today().strftime('%Y-%m-%d')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    steps = models.PositiveIntegerField()
    miles = models.DecimalField(max_digits=5, decimal_places=2)
    flights_climbed = models.PositiveIntegerField()
    restingHR = models.PositiveIntegerField()
    def __str__(self):
        return str(self.user) + ' - ' + self.date + ' data '

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = datetime.today().strftime('%Y-%m-%d')
    workout = models.TextField()
    intensity = models.TextField()
    reps = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return str(self.user) + ' - ' + self.workout + ' - ' + self.date
