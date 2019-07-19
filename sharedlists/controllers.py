from sqlalchemy import func
from nanohttp import text, HTTPBadRequest, context, HTTPNotFound, HTTPForbidden
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from .models import User, Item


CR = '\n'


class Root(RestController):

    @classmethod
    def _get_current_user(cls):
        if not hasattr(context, 'identity') or context.identity is None:
            return None

        principal = context.identity
        return DBSession.query(User) \
            .filter(User.id == principal.payload.get('id')) \
            .one_or_none()

    @classmethod
    def _get_items(cls, owner, listtitle, *, verbose=None):
        query = DBSession.query(Item) \
            .filter(Item.listownerid == owner) \
            .filter(Item.list == listtitle) \
            .order_by(Item.id)

        if verbose is None:
            format = lambda i: f'{i.title}'
        else:
            format = lambda i: f'{i.ownerid}\t\t{i.title}'

        for item in query:
            yield f'{format(item)}{CR}'

    @classmethod
    def _get_lists(cls, owner):
        query = DBSession \
            .query(Item.listownerid, Item.list) \
            .filter(Item.ownerid == owner) \
            .group_by(Item.listownerid, Item.list) \
            .order_by(Item.list)

        if not query.count():
            yield ''
            return

        for l in query:
            yield f'{l[0]}/{l[1]}{CR}'

    @text
    def info(self):
        from sharedlists import __version__ as appversion

        users = DBSession.query(User).count()
        lists = DBSession.query(Item.listownerid, Item.list) \
            .group_by(Item.listownerid, Item.list).count()

        result = [
            f'Shared Lists v{appversion}',
            f'Total Lists: {users}',
            f'Total Users: {lists}',
        ]

        me = self._get_current_user()
        if me is not None:
            mylists = DBSession.query(Item.listownerid, Item.list) \
                .filter(Item.listownerid == me.id) \
                .group_by(Item.listownerid, Item.list).count()
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
    @authorize
    @commit
    def append(self, listownerid, listtitle, itemtitle):
        me = self._get_current_user()
        item = Item(
            listownerid=listownerid,
            list=listtitle,
            title=itemtitle
        )
        me.items.append(item)
        DBSession.flush()
        return ''.join((str(item), CR))

    @text
    @authorize
    @commit
    def delete(self, listowner, listtitle, itemtitle):
        item = DBSession.query(Item) \
            .filter(Item.listownerid == listowner) \
            .filter(Item.list == listtitle) \
            .filter(Item.title == itemtitle) \
            .one_or_none()

        if item is None:
            raise HTTPNotFound()

        me = self._get_current_user()
        if me.id != item.ownerid or me.id != item.listownerid:
            raise HTTPForbidden()

        DBSession.delete(item)
        return ''.join((str(item), CR))

    @text
    def get(self, owner=None, listtitle=None, *, verbose=None):
        if owner and listtitle:
            return self._get_items(owner, listtitle, verbose=verbose)

        if owner:
            return self._get_lists(owner)

