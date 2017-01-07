import os
import json
from subprocess import call

from . import *

class Command(ParsingBaseCommand):
    help = 'executes webpack to build project assets (JS/CSS). Any arguments that are '\
           'not captured by the command is passed unaltered to webpack'

    def parse(self, parser, argv):
        args, unknown = parser.parse_known_args(argv)
        self.unknown_arguments = unknown
        return args

    def add_arguments(self, parser):
        parser.add_argument('applabel',
                            help='the app for which to compile webpack assets')

        parser.add_argument('--webpack-help',
                            help="executes webpack's help command (so as not to interfere with django's)",
                            action='store_true')

    def handle(self, *args, **options):
        from django.apps import apps
        from webpack_helper.conf import settings

        # --- load django settings settings
        NODE_BIN = os.path.join(settings.NODE_MODULES, '.bin')

        # ensure paths exist
        mkdirs(settings.CONFIG_DIR)
        mkdirs(settings.STATS_DIR)
        mkdirs(settings.BUNDLE_DIR)

        # --- build app specific path
        app_label = options['applabel']
        WEBPACK_CONF_FILE = os.path.join(settings.CONFIG_DIR, app_label + '.json')
        WEBPACK_STATS_FILE = os.path.join(settings.STATS_DIR, app_label + '.json')

        app_config = apps.get_app_config(app_label)

        # --- generate a config file
        config = {}
        config['WEBPACK_EXTRA_MODULE_DIRECTORIES'] = [settings.NODE_MODULES]
        config['WEBPACK_PUBLIC_PATH'] = settings.PUBLIC_PATH
        config['WEBPACK_BUNDLE_DIR'] = settings.BUNDLE_DIR
        config['WEBPACK_STATS_FILE'] = WEBPACK_STATS_FILE

        with open(WEBPACK_CONF_FILE, 'w') as config_file:
            json.dump(config, config_file, indent=4)

        # --- prepare arguments for execution
        webpack = os.path.join(NODE_BIN, 'webpack')
        args = [webpack] + self.unknown_arguments
        if options['webpack_help']:
            args.append('--help')

        # --- prepare environment & call webpack
        with env(NODE_PATH=settings.NODE_MODULES,
                 DJANGO_WEBPACK_CONFIG=WEBPACK_CONF_FILE):
            with cd(app_config.path):
                    call(args)
