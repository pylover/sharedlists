"""
The client utility fo sharedlists
"""
import os
import sys
import functools
from os import path
from getpass import getpass

from pymlconf import DeferredRoot
from easycli import Root, SubCommand, Argument
import requests


error = functools.partial(print, file=sys.stderr)
success = functools.partial(print, end='')
settings = DeferredRoot()
CONFIGFILE = path.join(os.environ['HOME'], '.beerc')
BUILTIMSETTINGS = '''
url:
token:
'''


def dump_config():
    with open(CONFIGFILE, 'w') as f:
        f.write(settings.dumps())


def query(verb, path='/', form=None):
    kw = {}
    headers = {}
    if settings.token:
        headers['Authorization'] = settings.token

    if form:
        kw['data'] = form

    kw['headers'] = headers
    response = requests.request(
        verb.upper(),
        f'{settings.url}/{path}',
        **kw
    )

    if response.status_code != 200:
        error(response.status_code, response.reason)
        return

    return response.text


class Info(SubCommand):
    __command__ = 'info'
    __aliases__ = ['i', 'in', 'inf']

    def __call__(self, args):
        success(query('info'))


class Login(SubCommand):
    __command__ = 'login'
    __aliases__ = ['lo', 'log', 'logi']
    __arguments__ = [
        Argument('username', help='Username or email')
    ]
    def __call__(self, args):
        password = getpass()
        settings.token = query('login', form=dict(
            email=args.username,
            password=password
        ))
        dump_config()


class Bee(Root):
    __help__ = 'Sharedlists client'
    __arguments__ = [
        Login,
        Info,
    ]

    def _execute_subcommand(self, args):
        settings.initialize(BUILTIMSETTINGS)
        if not path.exists(CONFIGFILE):
            dump_config()
        settings.load_file(CONFIGFILE)
        return super()._execute_subcommand(args)


if __name__ == '__main__':
    Bee().main(['lo', 'pylover'])

