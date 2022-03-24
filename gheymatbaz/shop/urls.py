from django.urls import path
from shop.views import test

urlpatterns = [
    path('', test)
]
