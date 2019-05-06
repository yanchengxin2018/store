from django.contrib.auth import get_user_model
import random
from rest_framework_jwt.settings import api_settings
from UserInfo.models import RolesModel
# from UserInfo.serializers import RolesSerializer


def test():
    pass


#从用户实例转化为token
def get_token_from_user(user_obj=None):
    '''
    从用户实例转化为token
    :param user_obj:用户实例
    :return:token
    '''
    payload = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode = api_settings.JWT_ENCODE_HANDLER
    data = payload(user_obj) # 把用户表转化为字典
    data['validate_sign']=user_obj.validate_sign
    token = jwt_encode(data) # 把字典转化为jwt字符串
    return token


#从token解析出用户实例
def get_user_from_token(token=None):
    '''
    从token解析出用户实例
    :param token: 字符串类型的jwt_token
    :return: 用户实例
    '''
    decode_handler = api_settings.JWT_DECODE_HANDLER
    try:
        data = decode_handler(token)
        id=data.get('user_id')
        user_obj=get_user_model().objects.filter(pk=id).first()
        return user_obj
    except:
        return None


#使当前用户实例的token无效化
def invalid_token(user_obj=None):
    '''
    使当前用户实例的token无效化
    :param user_obj: 用户实例
    :return: 返回bool状态,True为成功,False为失败
    '''
    if type(user_obj)==get_user_model():
        user_obj.validate_sign=get_num(10)
        user_obj.save()
        return True
    else:
        return False


#得到随机数量的数字字符串
def get_num(n):
    '''
    得到随机数量的数字字符串
    :param n: 要生成的随机数字字符串的长度
    :return: str类型的字符串
    '''
    return ''.join([str(random.randint(0,9)) for i in range(n)])


#得到一个唯一的username
def get_username():
    '''
    得到一个唯一的username
    :return: 一个用户表中不存在的username
    '''
    user = get_user_model()
    while True:
        username = get_num(10)
        if user.objects.filter(username=username):
            continue
        else:
            return username


#得到角色
def get_user_role(user):
    if not user:
        return '匿名用户'
    role_obj=user.rolesmodel_set.all().first()
    return role_obj.role_name if role_obj else '未定义角色用户'



















































