from rest_framework.views import exception_handler as exception_handler_0
from error.custom_errors import CustomStatus
from rest_framework.response import Response
import pickle
from error.models import ExceptionLogModel
from django.conf import settings
from Tools.base_tool import SendSMS


#把任意对象转化为二进制数据,不支持的类型取其__name__属性或者其__str__方法返回值.
def pickle_dumps(data_dict):
    try:
        return pickle.dumps(data_dict)
    except:
        pass
    data={}
    for key,value in data_dict.items():
        try:
            pickle.dumps({key:value})
        except:
            try:
                value='{}(原数据类型不支持pickle.dumps,已经取其__name__属性.数据原本的类型为{})'.format(
                    value.__name__,type(value))
            except:
                value = '{}(原数据类型不支持pickle.dumps,已经取其__str__方法返回值.数据原本的类型为{})'.format(
                    value.__str__(), type(value))
        data[key]=value
    return pickle.dumps(data)


#从request得到完整的url
def get_url(request):
    path=request.get_full_path()
    return path


#短信通知
def notice(info):
    send_obj=SendSMS(mobile='17686988582',data=info,log='调试')
    send_obj.send()


#处理(状态码异常对象)
def status_exception_handler(exception_obj,exception_kwargs):
    # write_log(exception_obj,exception_kwargs)
    request=exception_kwargs.get('request')
    view=exception_kwargs.get('view')
    url=get_url(request)
    post_data=pickle_dumps(request.data)
    header_data=pickle_dumps(request.META)
    user_obj=request.user
    cookie_data=pickle_dumps(request.COOKIES)
    exception_data=pickle_dumps(exception_obj.data)
    action=view.action
    exception_log_obj=ExceptionLogModel.objects.create(url=url,post_data=post_data,header_data=header_data,
        user_obj=user_obj,cookie_data=cookie_data,action=action,
        exception_data=exception_data,status=exception_obj.status)

    # send_info='{}-->{}\n{}\n{}\n{}\n'.format(action,url,request.data,user_obj,exception_obj.data)
    user_name=user_obj.name if user_obj else '匿名用户'
    send_info='\n{}\n{}\n{}'.format({'状态码':exception_obj.status},{'用户':user_name},exception_obj.data)
    if len(send_info)>139:
        send_info=send_info[:138]
    notice(send_info)
    return Response(exception_obj.data, status=exception_obj.status)


#未在计划内的异常
def other_exception_handler(exception_obj,exception_kwargs):
    request=exception_kwargs.get('request')
    url=get_url(request)
    post_data=pickle_dumps(request.data)
    header_data=pickle_dumps(request.META)
    user_obj=request.user
    cookie_data=pickle_dumps(request.COOKIES)
    exception_data=pickle.dumps(str(exception_obj))
    exception_log_obj=ExceptionLogModel.objects.create(url=url,post_data=post_data,header_data=header_data,
        user_obj=user_obj,cookie_data=cookie_data,exception_data=exception_data)
    if not settings.DEBUG:
        return Response('服务器繁忙', status=503)
    else:
        return exception_handler_0(exception_obj,exception_kwargs)


#为异常分配handler
def exception_handler(exception_obj,exception_kwargs):
    #状态码异常
    if (getattr(exception_obj,'is_default_status',False)) or (type(exception_obj) is CustomStatus):
        return status_exception_handler(exception_obj,exception_kwargs)
    #其他的异常
    else:

        return other_exception_handler(exception_obj,exception_kwargs)





