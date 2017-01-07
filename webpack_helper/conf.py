from __future__ import print_function
import sys
import os
import re

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class AttrView(object):
    def __init__(self, dictionary):
        self.__dictionary = dictionary

    def __contains__(self, key):
        return key in self.__dictionary

    def __setattr__(self, key, value):
        if key == '_' + type(self).__name__ + '__dictionary':
            object.__setattr__(self, key, value)
        else:
            self.__dictionary[key] = value

    def __getattr__(self, key):
        return self.__dictionary[key]

    def __iter__(self):
        for key in self.__dict__:
            yield key

    def __len__(self):
        return len(self.__dictionary)

    def __str__(self):
        return str('<AttrView '+str(self.__dictionary) + '>')


def gets(name, *default):
    if len(default) > 1:
        raise RuntimeError("Only a single default is allowed")
    return getattr(django_settings, name, *default)

PROJECT_ROOT = gets("BASE_DIR")

static_url = gets('STATIC_URL')
if not static_url.endswith('/'):
    static_url += '/'

defaults = {
   'NODE_MODULES': 'node_modules',
   'BASE_DIR': 'webpack',
   'BUNDLE_DIR': 'bundles/',
   'CONFIG_DIR': 'config/',
   'STATS_DIR': 'stats/',
   'STATIC_DIR': 'static/',
   'PUBLIC_PATH_BASE': gets('STATIC_URL')
}

settings_pre = dict(defaults)
settings_pre.update(getattr(django_settings, 'WEBPACK_HELPER', {}))

# --- check that setting names are correct
for key in settings_pre:
    if key not in defaults:
        msg = 'django-webpack-helper: setting %s is not a recognized setting'
        raise ImproperlyConfigured(msg % key)

# --- ensure that all paths are absolute
settingsdict = {}

pre = AttrView(settings_pre)
settings = AttrView(settingsdict)

def relto_or_abs(path, relto=PROJECT_ROOT):
    """
    if path is not absolute, return it relative to relto
    else keep it as is.
    """
    if not os.path.isabs(path):
        return os.path.join(relto, path)
    return path

def relto(root, path, name):
    if os.path.isabs(path):
        msg = 'django-webpack-helper: setting %s should be a relative path, but got %s.'
        raise ImproperlyConfigured(msg % (name, path))
    return os.path.join(root, path)


# --- make all paths absolute
settings.PROJECT_BASE = PROJECT_ROOT

settings.NODE_MODULES = relto_or_abs(pre.NODE_MODULES)
settings.BASE_DIR = relto_or_abs(pre.BASE_DIR)

settings.CONFIG_DIR = relto(settings.BASE_DIR, pre.CONFIG_DIR, 'CONFIG_DIR')
settings.STATS_DIR = relto(settings.BASE_DIR, pre.STATS_DIR, 'STATS_DIR')
settings.STATIC_DIR = relto(settings.BASE_DIR, pre.STATIC_DIR, 'STATIC_DIR')
settings.BUNDLE_DIR = relto(settings.STATIC_DIR, pre.BUNDLE_DIR, 'BUNDLE_DIR')

settings.PUBLIC_PATH = pre.PUBLIC_PATH_BASE + '/' + pre.BUNDLE_DIR + '/'
settings.PUBLIC_PATH = re.sub(r'/{2,}', '/', settings.PUBLIC_PATH)

if not os.path.exists(settings.NODE_MODULES):
    msg = "WEBPACK_HELPER['NODE_MODULES'] path does not exist: %s \n"\
          "Set WEBPACK_HELPER['NODE_MODULES'] to a valid `node_modules/` directory "\
          "in your `settings.py` file."
    msg = msg % settings.NODE_MODULES
    raise ImproperlyConfigured(msg)

