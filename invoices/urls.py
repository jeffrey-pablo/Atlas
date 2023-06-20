from django.urls import path
from . import views

urlpatterns = [
    path('table/', views.invoices_table_view, name="invoices_table"),
    path('index/', views.invoices_index_view, name="invoices_index"),
]