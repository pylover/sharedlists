from nanohttp import text, HTTPBadRequest, context
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from .models import User, List


CR = '\r\n'


class Root(RestController):

    @staticmethod
    def ensure_member(id_):
        member = DBSession.query(Member).filter(Member.id == id_).one_or_none()

        if member is None:
            raise HTTPNotFound(f'No member with id {id}')

        return member

    @text
    def info(self):
        from sharedlists import __version__ as appversion

        users = DBSession.query(User).count()
        lists = DBSession.query(List).count()
        result = [
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

