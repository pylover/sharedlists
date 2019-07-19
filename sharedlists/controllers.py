from sqlalchemy import func
from nanohttp import text, HTTPBadRequest, context, HTTPNotFound, HTTPForbidden
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from .models import User, Item


CR = '\n'


class Root(RestController):

    @staticmethod
    def ensure_user(id_):
        user = DBSession.query(Member).filter(Member.id == id_).one_or_none()

        if user is None:
            raise HTTPNotFound(f'No user with id {id}')

        return user

    @text
    def info(self):
        from sharedlists import __version__ as appversion

        users = DBSession.query(User).count()
        lists = DBSession.query(Item.listownerid, Item.list) \
            .group_by(Item.listownerid, Item.list).count()

        result = [
            f'',
            f'Shared Lists v{appversion}',
            f'Total Lists: {users}',
            f'Total Users: {lists}',
        ]

        me = User.get_current(DBSession)
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
    @commit
    @authorize
    def append(self, listownerid, listtitle, itemtitle):
        me = User.get_current(DBSession)
        item = Item(
            listownerid=listownerid,
            list=listtitle,
            title=itemtitle
        )
        me.items.append(item)
        DBSession.flush()
        yield CR
        yield str(item)
        yield CR

    @text
    @commit
    @authorize
    def delete(self, listowner, listtitle, itemtitle):
        item = DBSession.query(Item) \
            .filter(Item.listownerid == listowner) \
            .filter(Item.list == listtitle) \
            .filter(Item.title == itemtitle) \
            .one_or_none()

        if item is None:
            raise HTTPNotFound()

        me = User.get_current(DBSession)
        if me.id != item.ownerid or me.id != item.listownerid:
            raise HTTPForbidden()

        DBSession.delete(item)
        yield CR
        yield str(item)
        yield CR

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

        yield CR
        for item in query:
            yield f'{format(item)}{CR}'

    @classmethod
    def _get_lists(cls, owner):
        query = DBSession \
            .query(Item.list, func.count(Item.title)) \
            .filter(Item.listownerid == owner) \
            .group_by(Item.list) \
            .order_by(Item.list)

        yield CR
        for l in query:
            yield f'({l[1]})\t\t{l[0]}{CR}'


    @text
    def get(self, owner, listtitle=None, *, verbose=None):
        if owner and listtitle:
            return self._get_items(owner, listtitle, verbose=verbose)

        if owner:
            return self._get_lists(owner)

