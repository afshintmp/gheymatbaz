import json
from django.core import serializers
from json import JSONEncoder


def check_is_superuser(user):
    return user.is_superuser
