import os
from django.conf import settings

# Ensure the settings module is loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

import django
django.setup()

static_dir = os.path.join(settings.BASE_DIR, 'static')
for root, dirs, files in os.walk(static_dir):
    for file in files:
        print(os.path.join(root, file))
