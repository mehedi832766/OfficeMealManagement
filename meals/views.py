from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import MealOrder, DayMenu, MenuItem
from accounts.models import Employee
from .serializers import MealOrderSerializer, MenuItemSerializer
from datetime import time
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class PlaceOrderView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    serializer_class = MealOrderSerializer

    def post(self, request):
        # user = Employee.objects.first()
        user = request.user
        now = timezone.localtime()
        today = now.date()

        cutoff_time = time(18, 25)  # 11:00 AM

        # block after 11 AM
        if now.time() > cutoff_time:
            return Response(
                {"error": "Order window closed after 11:00 AM"},
                status=400
            )

        # prevent duplicate
        if MealOrder.objects.filter(employee=user, date=today).exists():
            return Response(
                {"error": "Already ordered"},
                status=400
            )

        try:
            day_menu = DayMenu.objects.get(day_of_week=today.weekday())
        except DayMenu.DoesNotExist:
            return Response(
                {"error": "No menu set for today"},
                status=400
            )

        MealOrder.objects.create(
            employee=user,
            day_menu=day_menu,
            date=today
        )

        return Response({"message": "Order placed"})
    
class TodayMenuView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        today = timezone.localdate()
        day_of_week = today.weekday()

        try:
            day_menu = DayMenu.objects.get(day_of_week=day_of_week)
        except DayMenu.DoesNotExist:
            return Response({"error": "No menu set"}, status=400)

        items = MenuItem.objects.filter(day_menu=day_menu).order_by('sort_order')
        serializer = MenuItemSerializer(items, many=True)

        return Response({
            "date": today,
            "day": day_of_week,
            "menu": serializer.data
        })    
    


class DailySummaryView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]


    def get(self, request):
        today = timezone.localdate()

        orders = MealOrder.objects.filter(date=today)

        total_orders = orders.count()

        employee_list = list(
            orders.values_list("employee__full_name", flat=True)
        )

        return Response({
            "date": today,
            "total_orders": total_orders,
            "employees": employee_list
        })
    


class MonthlyReportView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]


    def get(self, request):
        today = timezone.localdate()

        current_month = today.month
        current_year = today.year

        orders = MealOrder.objects.filter(
            date__month=current_month,
            date__year=current_year
        )

        total_orders = orders.count()

        employee_wise = (
            orders
            .values("employee__email")
            .annotate(total_orders=Count("id"))
            .order_by("-total_orders")
        )

        result = []

        for item in employee_wise:
            result.append({
                "employee": item["employee__email"],
                "total_orders": item["total_orders"]
            })

        return Response({
            "month": current_month,
            "year": current_year,
            "total_orders": total_orders,
            "employee_wise": result
        })