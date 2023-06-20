from django.urls import path
from . import views

urlpatterns = [
    path('new_report/', views.progress_reports_form_view, name="progress_reports_form"),
    path('list/', views.progress_reports_list_view, name="progress_reports_list"),
    path('submit_confirmation/', views.progress_reports_confirmation_view, name="progress_reports_confirmation"),
    path('index/', views.progress_reports_index_view, name="progress_reports_index"),
]