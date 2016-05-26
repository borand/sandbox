from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets, routers
from sensordata import models

# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class DeviceInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DeviceInstance
        fields = ('serial_number', 'active', 'private', 'update_rate')

# ViewSets define the view behavior.
class DeviceInstanceViewSet(viewsets.ModelViewSet):
    queryset         = models.DeviceInstance.objects.all()
    serializer_class = DeviceInstanceSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer    