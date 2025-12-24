# ============ reports/urls.py ============
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/new/', views.create_report, name='create_report'),
    path('reports/<str:case_number>/', views.report_detail, name='report_detail'),
]