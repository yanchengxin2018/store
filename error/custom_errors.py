
#可以自定义状态码的异常
class CustomStatus(Exception):
    default_detail = {'error':'服务器捕捉到了这个异常,但是没有提供更多错误信息'}
    default_status =501

    def __init__(self,data=None,status=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=status if (status is not None) else self.default_status


class Status_400(Exception):
    default_detail = {'error':'语义有误,或请求参数有误.当前请求无法被服务器理解.除非进行修改,否则客户端不应该重复提交这个请求.'}
    default_status =400
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_401(Exception):
    default_detail = {'error':'当前请求需要用户验证.'}
    default_status =401
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_402(Exception):
    default_detail = {'error':'备用的状态码.'}
    default_status =402
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_403(Exception):
    default_detail = {'error':'服务器已经理解请求，但是拒绝执行它.'}
    default_status =403
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_404(Exception):
    default_detail = {'error':'资源没有被找到.'}
    default_status =404
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_503(Exception):
    default_detail = {'error':'服务器捕捉到了这个异常,但是没有提供更多错误信息'}
    default_status =503
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_200(Exception):
    default_detail = {'error':'在任意位置强制返回资源,但未定义数据'}
    default_status =200
    is_default_status=True

    def __init__(self,data=None):
        self.data=data if (data is not None) else self.default_detail
        self.status=self.default_status


class Status_204(Exception):
    #服务器成功处理了请求，但不需要返回任何实体内容
    default_detail = None
    default_status =204
    is_default_status=True

    def __init__(self):
        self.data=self.default_detail
        self.status=self.default_status













