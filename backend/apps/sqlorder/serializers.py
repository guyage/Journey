# coding=utf-8
from rest_framework import serializers
from sqlorder.models import *
from django.db.models import Q
from workflow.models import ApprovalGroup
import json

class SqlOrderTypeSerializer(serializers.ModelSerializer):

    first_approver = serializers.SlugRelatedField(read_only=True,slug_field='approver_group_name')
    second_approver = serializers.SlugRelatedField(read_only=True,slug_field='approver_group_name')
    dba_approver = serializers.SlugRelatedField(read_only=True,slug_field='approver_group_name')
    class Meta:
        model = SqlOrderType
        fields = ('id','ordertype','first_approver','second_approver','dba_approver','is_auto','is_file','comment')

class SqlFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SqlFile
        fields = "__all__"


class SqlTextSerializer(serializers.ModelSerializer):

    execinfo = serializers.SerializerMethodField('get_sql_execinfo')
    class Meta:
        model = SqlText
        fields = ('id','exectime','execinfo')
    def get_sql_execinfo(self,obj):
        if (obj.info):
            sql_execinfo = eval(obj.info)
        else:
            sql_execinfo = []
        return sql_execinfo

class SqlOrderSerializer(serializers.ModelSerializer):

    ordertypename = serializers.SerializerMethodField('get_ordertype_name')
    have_step = serializers.SerializerMethodField('get_step_count')
    class Meta:
        model = SqlOrder
        fields = ('id','title','ordertype','ordertypename','have_step','approver_group','status','creator','operator','create_time','update_time')
    def get_ordertype_name(self,obj):
        if (obj.ordertype):
            ordertypename = obj.ordertype.ordertype
        else:
            ordertypename = ''
        return ordertypename
    def get_step_count(self,obj):
        count = 1
        if (obj):
            count = obj.sqlorder_state.all().count()
        return count

class SqlOrderDetailSerializer(serializers.ModelSerializer):

    ordertype_info = serializers.SerializerMethodField('get_ordertypeinfo')
    approvergroup_name = serializers.SerializerMethodField('get_approver_group_name')
    sql_data = serializers.SerializerMethodField('get_sqltext')
    sqlorderstate = serializers.SerializerMethodField('get_sqlorder_state')
    ordertypename = serializers.SerializerMethodField('get_ordertype_name')
    sql_file = serializers.SerializerMethodField('get_sqlfile')
    class Meta:
        model = SqlOrder
        fields = ('id','title','ordertype','ordertypename','sql_file','ordertype_info','approvergroup_name','sql_data','status','sqlorderstate','creator','operator','create_time','update_time')
    def get_ordertype_name(self,obj):
        if (obj.ordertype):
            ordertypename = obj.ordertype.ordertype
        else:
            ordertypename = ''
        return ordertypename
    def get_ordertypeinfo(self,obj):
        ordertypeinfo = {'create':'开发','exec':'Inception','check':'开发','done':'系统'}
        if (obj.ordertype):
            # ordertypeinfo = SqlOrderTypeSerializer(obj.ordertype.values('first_approver','second_approver','dba_approver')).data
            ortertype_id = obj.ordertype.id
            ordertypeinfo_obj = SqlOrderType.objects.values('first_approver','second_approver','dba_approver').get(Q(id=ortertype_id))
            for k,v in ordertypeinfo_obj.items():
                if (v):
                    ordertypeinfo[k] = ApprovalGroup.objects.values('approver_group_name').get(Q(id=v))['approver_group_name']
                    # ordertypeinfo_obj[k] = ApprovalGroup.objects.values('approver_group_name').get(Q(id=v))['approver_group_name']
        else:
            ordertypeinfo = {'create':'开发','exec':'Inception','check':'开发','done':'系统'}
        return ordertypeinfo
    def get_approver_group_name(self,obj):
        if (obj.approver_group):
            approver_group_name = obj.approver_group.approver_group_name
        else:
            approver_group_name = ''
        return approver_group_name
    def get_sqltext(self,obj):
        sql_data = []
        obj.sqlorder_sqltext.all()
        for sql in obj.sqlorder_sqltext.all():
            sql_data.append({'id':sql.id,'inst':sql.instid.inst_name,'dbname':sql.dbname,'sql':sql.sqltext,'sqlstatus':sql.sqlstatus})
        return sql_data
    def get_sqlfile(self,obj):
        sql_file = []
        for sql in obj.sqlorder_sqlfile.all():
            print (sql)
            sql_file.append({'id':sql.id,'sqlfileurl':sql.sqlfileurl,'sqlfile':sql.sqlfile})
        return sql_file
    def get_sqlorder_state(self,obj):
        sqlorder_state = []
        states = obj.sqlorder_state.all().order_by('id')
        for state in states:
            sqlorder_state.append({'action':state.action,'status':state.status,'operator':state.operator,'create_time':state.create_time})
        return sqlorder_state
        

