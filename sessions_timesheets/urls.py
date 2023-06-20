from rest_framework.routers import DefaultRouter
from . import views
from .views import SessionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('sessions', SessionViewSet)

urlpatterns = [
    path('',include(router.urls)),

    path('session/', views.sessions_form_view, name="sessions_form"),
    path('sessions_detail/', views.sessions_detail_view, name="sessions_detail"),
    path('sessions_index/', views.sessions_index_view, name="sessions_index"),
    path('timesheets_index/', views.timesheets_index_view, name="timesheets_index"),
    path('timesheets_table/', views.timesheets_table_view,name='timesheets_table'),
]