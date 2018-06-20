"""
WSGI config for inventoryos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from subprocess import call

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventoryos.settings")

# startup code
# Start mjpg video streaming
print('Try to start mjpg_streamer')
call('/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video0 -q 80 -y -n -f 5" -o "output_http.so -p 8081 -w /usr/local/share/mjpg-streamer/www" &', shell=True)
call('/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video1 -q 80 -y -n -f 5" -o "output_http.so -p 8082 -w /usr/local/share/mjpg-streamer/www" &', shell=True)
call('/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video2 -q 80 -y -n -f 5" -o "output_http.so -p 8083 -w /usr/local/share/mjpg-streamer/www" &', shell=True)
call('/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video3 -q 80 -y -n -f 5" -o "output_http.so -p 8084 -w /usr/local/share/mjpg-streamer/www" &', shell=True)
print('Start 4 mjpg_streamer on port 8081~8084')

application = get_wsgi_application()
