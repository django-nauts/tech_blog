from . import views
from django.urls import path

app_name='account'

urlpatterns = [
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout_page'),
    path('register', views.register_user, name='register_page'),
    path('activate-account/<email_active_code>', views.activate_user_account, name='activate_account'),
    path('forget-pass', views.forget_password, name='forget_pass_page'),
    path('reset-pass/<active_code>', views.reset_password, name='reset_pass_page'),
]