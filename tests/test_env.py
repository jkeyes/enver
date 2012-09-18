#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import enver
import os
import sys

from nose.tools import raises
from nose.tools import ok_
from StringIO import StringIO


class Env(object):
    VAR_1 = "Variable 1 Help"
    VAR_2 = "Variable 2 Help"
    REQUIRED = ['VAR_1']


class NotRequiredEnv(object):
    VAR_3 = "Variable 3 Help"


@raises(EnvironmentError)
def test_check_env():
    env = Env()
    # if all of the variables aren't in the environment
    # raise an EnvironmentError
    for var in env.REQUIRED:
        if var in os.environ:
            del os.environ[var]

    # check the environment
    enver.check_env(env)


def test_check_env_no_required():
    env = NotRequiredEnv()
    # check the environment, and don't raise an error as none of
    # the environment variables are required by the app runtime
    enver.check_env(env)


def test_help_env():
    # test the help env output
    io = StringIO()

    # set the application environment spec (see Env above)
    enver._Enver.ENV = Env()

    # dump the environment help into io
    enver.help_env(output=io)

    # verify the output
    output = io.getvalue()
    ok_('VAR_1: Variable 1 Help' in output)
    ok_('VAR_2: Variable 2 Help' in output)


def test_help_env_parser():
    # test running the parser from the command line with system
    # arguments and environment variables

    sys.argv = ['', 'help']

    stdout = sys.stdout  # save stdout
    sys.stdout = StringIO()  # redirect stdout

    # run the parser
    enver.run(Env())

    # check the output
    output = sys.stdout.getvalue()
    ok_('VAR_1: Variable 1 Help' in output)
    ok_('VAR_2: Variable 2 Help' in output)

    # reset sys.stdout
    sys.stdout = stdout


def test_dump_env():
    # test the dump_env output
    io = StringIO()

    # set the application environment spec (see Env above)
    enver._Enver.ENV = Env()

    # set an environment variable
    os.environ['VAR_1'] = 'ABC'
    try:
        # dump the environment into io
        enver.dump_env(output=io)

        # verify the output
        output = io.getvalue()
        ok_('VAR_1=ABC' in output)
        ok_('VAR_2=__NOT SET__' in output)
    finally:
        # clean up the environment
        del os.environ['VAR_1']


def test_dump_env_parser():
    # test running the parser from the command line with system
    # arguments and environment variables

    sys.argv = ['', 'dump']

    stdout = sys.stdout  # save stdout
    sys.stdout = StringIO()  # redirect stdout

    # run the parser
    enver.run(Env())

    # no environment variables means nothing set
    output = sys.stdout.getvalue()
    ok_('VAR_1=__NOT SET__' in output)
    ok_('VAR_2=__NOT SET__' in output)

    # reset the output buffer
    sys.stdout.truncate(0)

    # set an environment variable
    os.environ['VAR_2'] = '123'
    try:
        # run the parser
        enver.run(Env())

        # one of the environment variables is set
        output = sys.stdout.getvalue()
        ok_('VAR_1=__NOT SET__' in output)
        ok_('VAR_2=123' in output)
    finally:
        # clean up the environment
        del os.environ['VAR_2']

    # reset sys.stdout
    sys.stdout = stdout
