from django.urls import path
from shop.views import single_product

urlpatterns = [
    path('1/', single_product)
]
