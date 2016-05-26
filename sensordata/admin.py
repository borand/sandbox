from django.contrib import admin
from sensordata.models import Units
from sensordata.models import TimeStamp
from sensordata.models import PhysicalSignal
from sensordata.models import Manufacturer
from sensordata.models import Device
from sensordata.models import DeviceGateway
from sensordata.models import Location
from sensordata.models import DeviceInstance
from sensordata.models import DataValue
from sensordata.models import DataObject
from sensordata.models import Note

# from sensordata.models import DataFile
# from sensordata.models import DeviceSystem
# from sensordata.models import DataValueSet
#
    
class DataValueAdmin(admin.ModelAdmin):
    list_display  = ['data_timestamp','device_instance','value']
    list_filter   = ('device_instance','device_instance__location','device_instance__serial_number')
#
class DeviceGatewayAdmin(admin.ModelAdmin):
    list_display  = ['name','address','port','active','protocol','process_pid']
    list_editable = ['active']
    list_filter   = ('active','protocol',)
#
class DeviceInstanceAdmin(admin.ModelAdmin):
    list_display  = ['device','serial_number','gateway','location','physical_signal','active','private','accept_from_gateway_only','update_rate','update_rate_max','max_range','min_range','update_threshold']
    list_editable = ['device','serial_number','active','private','accept_from_gateway_only','update_rate','update_rate_max','max_range','min_range','update_threshold']
    list_filter   = ['user','active','device','gateway','location']
    
class DeviceAdmin(admin.ModelAdmin):
    list_display  = ['device_name','model_number','units','manufacturer','actuator']
    list_editable = []
    list_filter   = ['manufacturer','device_name','model_number','actuator']
 
class DataObjectAdmin(admin.ModelAdmin):
    list_display  = ['data_timestamp','device_instance','value']
 
admin.site.register(Units)
admin.site.register(TimeStamp)
admin.site.register(PhysicalSignal)
admin.site.register(Manufacturer)
admin.site.register(Device,DeviceAdmin)
admin.site.register(DeviceGateway,DeviceGatewayAdmin)
admin.site.register(Location)
admin.site.register(DeviceInstance, DeviceInstanceAdmin)
admin.site.register(DataValue, DataValueAdmin)
admin.site.register(Note)
admin.site.register(DataObject, DataObjectAdmin)
#admin.site.register(DeviceSystem)
#admin.site.register(DataValueSet)