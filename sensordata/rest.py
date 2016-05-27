import time
import datetime
from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets, routers
from rest_framework.views import APIView
from sensordata import models

from rest_framework import generics
from rest_framework.decorators import api_view
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

class DataValueSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.DataValue

class DataValueList(viewsets.ModelViewSet):
    #permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset         = models.DataValue.objects.all()    
    serializer_class = DataValueSerializer

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

class DataValuePairSerializer2(serializers.Serializer):
    """
    Adaptation of tutorial example to Units.
    based on http://django-rest-framework.org/tutorial/1-serialization.html
    """
 
    data_timestamp = serializers.DateTimeField()
    value          = serializers.FloatField()

    @property
    def data(self):

        to = time.time()
        print("Found %d items matching criteria " % self.object.count())
        values_list = self.object.values_list('data_timestamp__measurement_timestamp','value')    
        v = self.object.values_list('value',flat=True)
        t = self.object.values_list('data_timestamp__measurement_timestamp',flat=True)
        print("Making the list        = %.3f" % (time.time() - to))

        print("Preparing array for json transmision")
        data = []
        for data_pt in values_list:        
            data.append([time.mktime(data_pt[0].timetuple()),data_pt[1]])

        print("Making value pair list = %.3f" % (time.time() - to))
        return data

class DataValueForDevDetail(generics.ListAPIView):
    #permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class   = DataValuePairSerializer2

    def get_queryset(self):

        print('get_queryset(kwargs= %s)' % str(self.kwargs))
        to = time.time()
        serial_number = self.kwargs['serial_number']
        queryset = models.DataValue.objects.filter(device_instance__serial_number=serial_number).order_by('data_timestamp__measurement_timestamp')
        print("Query time             = %.3f" % (time.time() - to))        
        
        if self.kwargs.has_key('today'):
            print("Filtering: todays data")        
            queryset = queryset.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())

        if self.kwargs.has_key('from') and self.kwargs.has_key('to'):
            print("Filtering: from %s to %s" % (self.kwargs.has_key('from'), self.kwargs.has_key('to')))
            start_date = datetime.datetime.strptime(self.kwargs['from'].split('.')[0],"%Y-%m-%d")
            end_date   = datetime.datetime.strptime(self.kwargs['to'].split('.')[0],"%Y-%m-%d")
            queryset = queryset.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))

        return queryset    