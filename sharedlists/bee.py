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
from itertools import groupby

from pymlconf import DeferredRoot
from easycli import Root, SubCommand, Argument
import requests


#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


error = functools.partial(print, file=sys.stderr)
success = functools.partial(print, end='')
settings = DeferredRoot()
CACHEPATH = path.join(os.environ['HOME'], '.cache', 'bee')
CACHEFILE = path.join(CACHEPATH, 'items')
CONFIGFILE = path.join(os.environ['HOME'], '.beerc')
BUILTIMSETTINGS = '''
  url: http://localhost:5555
  sslverify: true
  username:
  token:
'''

log = open('log', 'w')

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
        error(response.status_code, response.reason, '')
        return ''

    return response.text


class Cache:
    dirty = False
    lists = []
    items = []

    def __init__(self):
        self.loadfromfile()

    def loadfromfile(self):
        if not path.exists(CACHEFILE):
            os.makedirs(path.dirname(CACHEFILE), exist_ok=True)
            return

        with open(CACHEFILE) as f:
            self.items = sorted(
                [i.strip().split('/', 1) for i in f.readlines()]
            )

            self.lists = list(i[0] for i in groupby(self.items, lambda x: x[0]))

    def refresh(self):
        with open(CACHEFILE, 'w') as f:
            data = query('get', 'all')
            f.write(data)

        self.loadfromfile()
        self.dirty = False

    def invalidate(self):
        self.dirty = True

    def ensure(self):
        if self.dirty:
            self.refresh()

    def getlists(self, **kw):
        return self.lists

    def getitems(self, prefix, action, parser, parsed_args):
        list_ = parsed_args.list
        if not list_:
            return (i[1] for i in self.items)

        return (i[1] for i in self.items if i[0] == list_)


cache = Cache()


class Delete(SubCommand):
    __command__ = 'delete'
    __aliases__ = ['d']
    __arguments__ = [
        Argument(
            'list',
            default='',
            help='example: foo',
            completer=cache.getlists
        ),
        Argument(
            'item',
            help='Item to delete',
            completer=cache.getitems
        )
    ]

    def __call__(self, args):
        success(query('delete', f'{args.list}/{args.item}'))
        cache.refresh()


class Append(SubCommand):
    __command__ = 'append'
    __aliases__ = ['add', 'a']
    __arguments__ = [
        Argument(
            'list',
            default='',
            help='example: foo',
            completer=cache.getlists
        ),
        Argument(
            'item',
            help='Item to add',
            completer=cache.getitems
        )
    ]

    def __call__(self, args):
        success(query('append', f'{args.list}/{args.item}'))
        cache.refresh()


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
            default='',
            help='example: foo',
            completer=cache.getlists
        )
    ]

    def __call__(self, args):
        success(query('get', 'all' if args.all else args.list))


class Info(SubCommand):
    __command__ = 'info'
    __aliases__ = ['i']

    def __call__(self, args):
        success(query('info'))
        cache.refresh()


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
    __completion__ = True
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
        return super().main(argv=argv)

    def __call__(self, args):
        success(query('get'))


if __name__ == '__main__':
    Bee().main(['s', 'foo'])

