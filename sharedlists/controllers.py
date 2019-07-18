from nanohttp import text
from restfulpy.controllers import RootController
from restfulpy.orm import DBSession

from .models import User, List


CR = '\r\n'


class Root(RootController):

    @text
    def info(self):
        from sharedlists import __version__ as appversion

        users = DBSession.query(User).count()
        lists = DBSession.query(List).count()

        return CR.join((
            f'Shared Lists v{appversion}',
            f'Total Lists: {users}',
            f'Total Users: {lists}',
            ''
        ))


