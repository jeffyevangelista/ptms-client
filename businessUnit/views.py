from rest_framework.viewsets import ModelViewSet
from .serializers import businessUnit_Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class BusinessUnit_view(ModelViewSet):
    serializer_class = businessUnit_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

    
