from rest_framework import serializers
from main.models import *
from django.conf import settings


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model=TestModel
        fields=('id','name',)






















