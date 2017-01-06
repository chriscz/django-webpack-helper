#!/usr/bin/env python
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'db.sqlite3')

class FakeSettings:
    BASE_DIR = BASE_DIR

    STATIC_URL = '/static/'

    INSTALLED_APPS = (
            'webpack_loader',
            'webpack_helper',
            'exampleapp'
    )
    SECRET_KEY = "x-uegdq_zqfp*l-r(tw(4k7@=-%a7g31ojrop0(g%_&$(i^ygn"

    DATABASES = {
        'default': {
            # Database Driver
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            # Database Name
            'NAME': DB_DIR,                          # Or path to database file if using sqlite3.
            'USER': '',                              # Not used with sqlite3.
            'PASSWORD': '',                          # Not used with sqlite3.
            'HOST': '',                              # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                              # Set to empty string for default. Not used with sqlite3.
        }
    }

    TIME_ZONE = 'Africa/Johannesburg'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

if __name__ == "__main__":
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        sys.modules["settings"] = FakeSettings
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
