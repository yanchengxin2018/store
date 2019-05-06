from rest_framework import serializers
from error.models import ExceptionLogModel
import pickle
import json


#日志序列化器
class ExceptionLogSerializer(serializers.ModelSerializer):

    user_name=serializers.SerializerMethodField()
    exception_data=serializers.SerializerMethodField()
    post_data=serializers.SerializerMethodField()
    get_data=serializers.SerializerMethodField()
    header_data=serializers.SerializerMethodField()
    cookie_data=serializers.SerializerMethodField()

    def get_exception_data(self, exceptionlog_obj):
        data=exceptionlog_obj.exception_data
        if not data:return ''
        return pickle.loads(data)

    def get_post_data(self, exceptionlog_obj):
        data=exceptionlog_obj.post_data
        if not data:return ''
        return pickle.loads(data)

    def get_get_data(self, exceptionlog_obj):
        data=exceptionlog_obj.get_data
        if not data:return ''
        return pickle.loads(data)

    def get_header_data(self, exceptionlog_obj):
        data = exceptionlog_obj.header_data
        if not data: return '空值'
        #解析成对象
        data = pickle.loads(data)
        #把对象里不能json的类型取其name
        new_data={}
        for key,value in data.items():
            try:
                json.dumps({key:value})
            except:
                value='{}(为了dumps成功,仅取了此对象的__name__属性。原类型为{})'.format(value.__name__,type(value))
            new_data[key]=value
        return new_data

    def get_cookie_data(self, exceptionlog_obj):
        data=exceptionlog_obj.cookie_data
        if not data:return ''
        a=pickle.loads(data)
        return a

    def get_user_name(self,exceptionlog_obj):
        if exceptionlog_obj.user_obj:
            return exceptionlog_obj.user_obj.name
        else:
            return None

    class Meta:
        model=ExceptionLogModel
        fields=('id','created_at','user_name','exception_data','url','status',
                'user_obj','post_data','get_data','cookie_data',
                'header_data',)






















