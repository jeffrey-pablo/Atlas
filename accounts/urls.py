from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from .views import SignUpView, SignUpCompleteView
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_complete/', SignUpCompleteView.as_view(), name='signup_complete'),
    path('edit_profile/', views.edit_profile_form_view, name="edit_profile"),
    path('edit_profile/done/', views.edit_profile_done_view, name="edit_profile_done"),
    path('index/', views.accounts_index_view, name="accounts_index"),
    # other paths...
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
