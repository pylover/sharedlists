from getpass import getpass

from restfulpy.orm import DBSession
from easycli import SubCommand, Argument

from .models import User


class AddUserSubCommand(SubCommand):
    __command__ = 'add'
    __help__ = 'Add a new user'
    __arguments__ = [
        Argument(
            'name',
            help='Username',
        ),
        Argument(
            'email',
            help='Email address',
        )
    ]

    def __call__(self, args):
        user = User(
            id=args.name,
            email=args.email,
            password=getpass()
        )
        DBSession.add(user)
        DBSession.commit()



class UserCommand(SubCommand):
    __command__ = 'user'
    __help__ = 'User administration'
    __arguments__ = [
        AddUserSubCommand,
    ]

