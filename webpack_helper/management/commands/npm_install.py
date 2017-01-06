from . import *
from django.core.exceptions import ImproperlyConfigured
from subprocess import call, CalledProcessError

class Command(ParsingBaseCommand):
    help = 'A wrapper for running npm install on a django app. Any arguments that are '\
           'not captured by the command is passed unaltered to npm'

    def parse(self, parser, argv):
        args, unknown = parser.parse_known_args(argv)
        self.unknown_arguments = unknown
        return args

    def add_arguments(self, parser):
        parser.add_argument('app',
                            help='the app for which to install dependencies')

    def npm_install_app(self, settings, appconfig):
        try:
            with env(NODE_PATH=settings.NODE_MODULES):
                with cd(settings.PROJECT_BASE):
                    call(['npm', 'install', appconfig.path] + self.unknown_arguments)
        except CalledProcessError as e:
            print('Are you sure Node Package Manager (NPM) is installed?')
            raise

    def handle(self, *args, **options):
        from django.apps import apps
        from webpack_helper.conf import settings
        self.npm_install_app(settings, apps.get_app_config(options['app']))
