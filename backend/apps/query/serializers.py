from rest_framework import serializers
from query.models import *

class QuerySqlLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuerySqlLog
        fields = ('id','operator','mysqlinst','dbname','sql','create_time')