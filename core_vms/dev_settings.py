# dev_settings.py

from .settings import *  # Import everything from main settings

DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow everything for local dev

# Use SQLite for local testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev.sqlite3',
    }
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}