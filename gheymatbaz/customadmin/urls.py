from django.urls import path
from customadmin.views import insert_product

urlpatterns = [
    path('', insert_product)
]
