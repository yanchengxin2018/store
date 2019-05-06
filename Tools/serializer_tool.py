


#从当前序列化器得到调用者视图的用户
def get_user_from_serializer(serializer_obj):
    try:
        user_obj=serializer_obj._kwargs.get('context').get('view').request.user
        return user_obj
    except:
        return None


#从当前序列化器得到调用者视图的实例
def get_view_from_serializer(serializer_obj):
    try:
        view_obj=serializer_obj._kwargs.get('context').get('view')
        return view_obj
    except:
        return None









