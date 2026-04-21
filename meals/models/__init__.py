from .day_menu import DayMenu
from .menu_item import MenuItem
from .meal_order import MealOrder


from django.contrib import admin


admin.site.register(DayMenu)
admin.site.register(MenuItem)
admin.site.register(MealOrder)