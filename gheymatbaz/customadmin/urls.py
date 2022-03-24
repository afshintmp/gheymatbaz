from django.urls import path
from customadmin.views import customadmin

urlpatterns = [
    path('', customadmin)
]
