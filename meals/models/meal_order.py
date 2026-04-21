from django.db import models
from django.conf import settings
from .day_menu import DayMenu
User = settings.AUTH_USER_MODEL



class MealOrder(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    day_menu = models.ForeignKey(DayMenu, on_delete=models.CASCADE)
    date = models.DateField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'date')