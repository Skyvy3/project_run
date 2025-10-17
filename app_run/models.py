from django.db import models
from django.contrib.auth.models import User

# Определяем варианты статусов
RUN_STATUS_CHOICES = [
    ('init', 'Initialization'),
    ('in_progress', 'In Progress'),
    ('finished', 'Finished'),
]

class Run(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=RUN_STATUS_CHOICES,
        default='init'
    )

class AthleteInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_info')
    weight = models.FloatField(null=True, blank=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"AthleteInfo for {self.user.username}"