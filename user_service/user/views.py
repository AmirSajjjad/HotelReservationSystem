from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)
    
    def get_object(self):
        user_id = self.request.user.id
        return get_object_or_404(User, id=user_id)
    