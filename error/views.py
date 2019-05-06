from rest_framework.viewsets import ModelViewSet,GenericViewSet as G,mixins as M
from error.models import ExceptionLogModel
from error.serializers import ExceptionLogSerializer
from error import custom_errors
import pickle
from rest_framework.response import Response


#访问日志
class ExceptionLogViewSet(G,M.ListModelMixin,M.RetrieveModelMixin,M.DestroyModelMixin):

    queryset = ExceptionLogModel.objects.all().order_by('-created_at')
    serializer_class = ExceptionLogSerializer
    def list(self, request, *args, **kwargs):
        # self.queryset.delete() #谨慎使用,删除所有异常记录
        return super().list(request, *args, **kwargs)

#制造一个异常
class CreateExceptionViewSet(G):

    serializer_class = ExceptionLogSerializer

    def list(self,request):
        raise custom_errors.Status_404('测试的错误提示：xxx')

    def create(self,request):
        raise custom_errors.Status_401






