from django.db import models
from .day_menu import DayMenu



class MenuItem(models.Model):
    day_menu = models.ForeignKey(DayMenu, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
