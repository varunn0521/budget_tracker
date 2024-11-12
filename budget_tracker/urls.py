# budget_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('tracker.urls')),  # Routes requests for 'accounts' to the tracker app
    path('', views.home, name='home'),  # Map root URL to the home view
]
