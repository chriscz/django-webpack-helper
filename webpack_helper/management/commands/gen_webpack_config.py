from . import *
from shutil import copy
import os

class Command(ParsingBaseCommand):
    help = 'creates a boilerplate webpack configuration file for your next webpack project.'

    def parse(self, parser, argv):
        args, unknown = parser.parse_known_args(argv)
        self.unknown_arguments = unknown
        return args

    def add_arguments(self, parser):
        parser.add_argument('config_name',
                            help='the full name of the configuration file (ending in js)')

    def handle(self, *args, **options):
        from django.apps import apps
        copy(os.path.join(BASEDIR, 'webpack.config.js'), options['config_name'])
