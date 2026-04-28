from django.urls import path
from .views import PlaceOrderView, TodayMenuView, DailySummaryView, MonthlyReportView

urlpatterns = [
    path('orders/place/', PlaceOrderView.as_view()),
    path('menu/today/', TodayMenuView.as_view()),
    path("admin/daily/", DailySummaryView.as_view()),
    path("admin/monthly/", MonthlyReportView.as_view()),
]