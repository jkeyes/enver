#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import sys
from os import environ


class _Enver(object):
    ENV = None


def _get_env_attrs(mod):
    """ Parse the environment module and don't include any private
    attributes or the special REQUIRED case. """

    attrs = []
    for v in dir(mod):
        if v[0] == '_':
            continue
        elif v == 'REQUIRED':
            continue
        else:
            attrs.append(v)
    return attrs


def check_env(env):
    """ Check the required variables listed in the specified environment
    module are present in the system environment. """

    if not hasattr(env, 'REQUIRED'):
        env.REQUIRED = tuple()

    missing_vars = [var for var in env.REQUIRED if var not in environ]
    if missing_vars:
        error_msg = "The following variables are required to run tesla:\n" \
                "    %s\n" % (",".join(missing_vars))
        raise EnvironmentError(error_msg)


def dump_env(args=None, output=None):
    """ Dump the environment to the specified output file. """

    if output is None:
        output = sys.stdout

    output.write('Environment:\n')

    for var in _get_env_attrs(_Enver.ENV):
        value = environ.get(var, '__NOT SET__')
        output.write('    %s=%s\n' % (var, value))


def help_env(args=None, output=None):
    """ Describe the environment for the app. """

    if output is None:
        output = sys.stdout

    output.write('App Environment:\n')

    for var in _get_env_attrs(_Enver.ENV):
        output.write('%s: %s\n' % (var, getattr(_Enver.ENV, var)))


def run(env):
    """ Run the command line programs. """

    _Enver.ENV = env

    import argparse

    parser = argparse.ArgumentParser(description='App Environment')
    subparsers = parser.add_subparsers(help='sub-command help')

    dump = subparsers.add_parser('dump',
            help='dump the app environment variables')
    dump.set_defaults(func=dump_env)
    help = subparsers.add_parser('help',
            help='describe the app environment')
    help.set_defaults(func=help_env)

    args = parser.parse_args()
    args.func(args)
