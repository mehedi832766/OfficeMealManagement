from rest_framework import serializers
from .models import MealOrder


from .models import MenuItem

class MealOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOrder
        fields = '__all__'
        read_only_fields = ['employee', 'date', 'ordered_at']

    def __str__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{days[self.day_of_week]} Menu"
    


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'category', 'sort_order']