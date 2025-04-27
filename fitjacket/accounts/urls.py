from django.urls import path
from . import views
from accounts.views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='accounts.password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
     path('generate/', views.workout_plan_form, name='workout_plan_form'),
    path('results/', views.workout_plan_results, name='workout_plan_results'),
]