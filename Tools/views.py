
from rest_framework.views import APIView
from django.shortcuts import render


#文档
class DocViewSet(APIView):
    def get(self,request):
        user_obj=request.user
        if user_obj:
            user_name=user_obj.name
            welcome=f'欢迎你,{user_name}!'
        else:
            user_name='游客'
            welcome = f'欢迎你,{user_name}! '




        return render(request,'doc.html',{})









