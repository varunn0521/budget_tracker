# budget_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('tracker.urls')),  
    path('', views.home, name='home'),
]