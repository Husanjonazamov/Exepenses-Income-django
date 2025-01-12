from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name='income'),
    path("add-income", views.add_income, name='add-income'),
    path("edit-income/<int:id>", views.income_edit, name='edit-income'),
    path("expenses-delete/<int:id>", views.delete_income, name='income-delete'),
    path('search-income', csrf_exempt(views.search_income), name='search_income'),
    path('income_source_summary/', csrf_exempt(views.income_source_summary), name='income_source_summary'),
    path("stats-income/", views.stats_viewIncome, name='stats-income'),
    path("export_csv/", views.export_csv, name='export-csv'),
    path("export_excel/", views.export_excel, name='export-excel'),
    path("export-pdf/", views.export_pdf, name='export-pdf'),
]
