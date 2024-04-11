from django.contrib import admin
from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
        path('', views.home, name='home'),
        path('login/', views.loginPage, name='login'),
        path('logout/', views.logoutUser, name='logout'),
        path('register/', views.register, name='register'),
        path('admin/', admin.site.urls),    
]