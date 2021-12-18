from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from module_user.models.User import User
from module_user.serializers.MeSerializer import MeSerializer


class MeViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = self.queryset.filter(pk=self.request.user.pk)
        return q
