from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import MealOrder, DayMenu
from accounts.models import Employee
from .serializers import MealOrderSerializer

class PlaceOrderView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MealOrderSerializer

    def post(self, request):
        user = Employee.objects.first()
        today = timezone.localdate()

        if MealOrder.objects.filter(employee=user, date=today).exists():
            return Response({"error": "Already ordered"}, status=400)

        day_menu = DayMenu.objects.get(day_of_week=today.weekday())

        MealOrder.objects.create(
            employee=user,
            day_menu=day_menu,
            date=today
        )

        return Response({"message": "Order placed"})