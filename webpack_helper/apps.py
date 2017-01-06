from django.apps import AppConfig
import os

base_path = os.path.dirname(os.path.abspath(__file__))


class WebpackHelperConfig(AppConfig):
    name = 'webpack_helper'
    label = 'webpack_helper'
