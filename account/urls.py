from . import views
from django.urls import path

app_name='account'

urlpatterns = [
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout_page'),
]