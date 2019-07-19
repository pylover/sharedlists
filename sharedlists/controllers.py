from nanohttp import text, HTTPBadRequest, context
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from .models import User, List


CR = '\n'


class Root(RestController):

    @staticmethod
    def ensure_user(id_):
        user = DBSession.query(Member).filter(Member.id == id_).one_or_none()

        if user is None:
            raise HTTPNotFound(f'No user with id {id}')

        return user

    @staticmethod
    def ensure_list(owner, title):
        list_ = DBSession.query(List).filter(List.title == title).one_or_none()

        if list_ is None:
            raise HTTPNotFound(f'List not found: {id}')

        return list_

    @text
    def info(self):
        from sharedlists import __version__ as appversion

        users = DBSession.query(User).count()
        lists = DBSession.query(List).count()
        result = [
            f'',
            f'Shared Lists v{appversion}',
            f'Total Lists: {users}',
            f'Total Users: {lists}',
        ]

        me = User.get_current(DBSession)
        if me is not None:
            mylists = me.lists.count()
            result.append(f'My Lists: {mylists}')

        result.append('')
        return CR.join(result)

    @text
    def login(self):
        email = context.form.get('email')
        password = context.form.get('password')

        def bad():
            raise HTTPBadRequest('Invalid email or password')

        if not (email and password):
            bad()

        principal = context.application \
            .__authenticator__ \
            .login((email, password))

        if principal is None:
            bad()

        return principal.dump()

    @text
    @commit
    @authorize
    def create(self, owner, title):
        me = User.get_current(DBSession)
        if me is None:
            raise HTTPUnauthorized()

        if me.id != owner:
            raise HTTPForbiden()

        newlist = List(title=title)
        me.lists.append(newlist)
        DBSession.flush()
        return str(newlist)

    @text
    @commit
    @authorize
    def append(self, owner, title, item):
        list_ = DBSession.query(List).filter(List.title == title).one_or_none()
        DBSession.add(newlist)
        return str(newlist)

