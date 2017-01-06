import sys
import os
from django.core.management.base import BaseCommand, CommandError
import django.core.management.base as base_management
from contextlib import contextmanager

__all__ = ['cd', 'env', 'mkdirs', 'ParsingBaseCommand', 'BASEDIR']
BASEDIR = os.path.dirname(os.path.abspath(__file__))

@contextmanager
def cd(path):
    old = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old)


@contextmanager
def env(env=None, **kwargs):
    env = env or {}
    env.update(kwargs)

    old_env = dict(os.environ)
    try:
        os.environ.update(env)
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# see https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#ref-basecommand-subclasses
class ParsingBaseCommand(BaseCommand):
    """
    Allows us to intercept parsing of commandline arguments
    """
    def parse(self, parser, argv):
        return parser.parse_args(argv[2:])

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])

        if self.use_argparse:
            options = self.parse(parser, argv[2:])
            cmd_options = vars(options)
            # Move positional args out of options to mimic legacy optparse
            args = cmd_options.pop('args', ())
        else:
            options, args = self.parse(parser, argv[2:])
            cmd_options = vars(options)
        base_management.handle_default_options(options)
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            if options.traceback or not isinstance(e, CommandError):
                raise
            # SystemCheckError takes care of its own formatting.
            if isinstance(e, base_management.SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)
        finally:
            base_management.connections.close_all()
