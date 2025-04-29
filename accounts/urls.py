# accounts/urls.py
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views import ResetView, MyPasswordResetView, register
from accounts.forms import CustomPasswordResetForm

auth_views.PasswordResetView.form_class = CustomPasswordResetForm


urlpatterns = [    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/', register, name='register'),
    path("password_reset/", MyPasswordResetView.as_view(template_name='registration/password_reset.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
