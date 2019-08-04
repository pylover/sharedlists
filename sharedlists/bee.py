"""
The client utility fo sharedlists
"""

import os
import sys
import urllib3
import argparse
import functools
from os import path
from getpass import getpass

from pymlconf import DeferredRoot
from easycli import Root, SubCommand, Argument
import requests


#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


error = functools.partial(print, file=sys.stderr)
success = functools.partial(print, end='')
settings = DeferredRoot()
CONFIGFILE = path.join(os.environ['HOME'], '.beerc')
BUILTIMSETTINGS = '''
  url: http://localhost:5555
  sslverify: true
  username:
  token:
'''


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if '/' not in values:
            values = f'{settings.username}/{values}'

        setattr(namespace, self.dest, values)


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

    kw['verify'] = settings.sslverify
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


class Delete(SubCommand):
    __command__ = 'delete'
    __aliases__ = ['d']
    __arguments__ = [
        Argument(
            'list',
            action=ListAction,
            default='',
            help='example: [username/]foo'
        ),
        Argument(
            'item',
            help='Item to delete'
        )
    ]

    def __call__(self, args):
        success(query('delete', f'{args.list}/{args.item}'))


class Append(SubCommand):
    __command__ = 'append'
    __aliases__ = ['add', 'a']
    __arguments__ = [
        Argument(
            'list',
            action=ListAction,
            default='',
            help='example: [username/]foo'
        ),
        Argument(
            'item',
            help='Item to add'
        )
    ]

    def __call__(self, args):
        success(query('append', f'{args.list}/{args.item}'))


class Show(SubCommand):
    __command__ = 'show'
    __aliases__ = ['s', 'l']
    __arguments__ = [
        Argument(
            '-a', '--all',
            action='store_true',
            help='Get all action',
        ),
        Argument(
            'list',
            nargs='?',
            action=ListAction,
            default='',
            help='example: [username/]foo'
        )
    ]

    def __call__(self, args):
        success(query('get', '' if args.all else args.list))


class Info(SubCommand):
    __command__ = 'info'
    __aliases__ = ['i']

    def __call__(self, args):
        success(query('info'))


class Login(SubCommand):
    __command__ = 'login'
    __arguments__ = [
        Argument('username', help='Username or email')
    ]
    def __call__(self, args):
        settings.token = query('login', form=dict(
            email=args.username,
            password=getpass()
        ))
        settings.username = args.username
        dump_config()


class Bee(Root):
    __help__ = 'Sharedlists client'
    __arguments__ = [
        Login,
        Show,
        Info,
        Append,
        Delete,
    ]

    def main(self, argv=None):
        settings.initialize(BUILTIMSETTINGS)
        if not path.exists(CONFIGFILE):
            dump_config()
        settings.load_file(CONFIGFILE)
        super().main(argv=argv)


if __name__ == '__main__':
    Bee().main(['s', 'foo'])

