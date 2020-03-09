# coding=utf-8
from rest_framework import serializers
from easyaudit.models import *

class CRUDEventSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,slug_field='username')
    content_type = serializers.SlugRelatedField(read_only=True,slug_field='model')
    class Meta:
        model = CRUDEvent
        fields = ('event_type','object_id','content_type','object_repr','object_json_repr','changed_fields','user','user_pk_as_string','datetime')