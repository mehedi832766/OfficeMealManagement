from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class DayMenu(models.Model):
    day_of_week = models.IntegerField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{days[self.day_of_week]} Menu"
