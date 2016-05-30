import os, sys

proj_path= os.path.dirname(os.path.abspath(__file__)) + "/.."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
print(proj_path)
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from data import models
from data import api_views
from data import data_utils


def print_device_instance():
	d = models.DeviceInstance.objects.all()
	print(d[0])

def submit_test():	
	out = data_utils.data_value_submission(datestamp="now", serial_number="0", data_value=0.5, remote_addr="127.0.0.1", is_obj=False)
	print(out)

if __name__ == '__main__':
	print_device_instance()
	submit_test()