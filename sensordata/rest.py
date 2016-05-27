import time
import datetime
from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets, routers
from rest_framework.views import APIView
from sensordata import models

from rest_framework import generics
from rest_framework.decorators import api_view
############################################################################
#
# Work in progress, connecting the entire site throught the rest api
#
############################################################################
# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    #device_instance = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = User
        fields = ('username')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

#class DeviceInstanceSerializer(serializers.HyperlinkedModelSerializer):
class DeviceInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceInstance

############################################################################
# ViewSets define the view behavior.
class DeviceInstanceViewSet(viewsets.ModelViewSet):
    queryset         = models.DeviceInstance.objects.all()
    serializer_class = DeviceInstanceSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset         = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset         = Group.objects.all()
    serializer_class = GroupSerializer