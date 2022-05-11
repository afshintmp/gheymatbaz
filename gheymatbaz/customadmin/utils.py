import json
from django.core import serializers
from json import JSONEncoder

from shop.models import Category


def check_is_superuser(user):
    return user.is_superuser

