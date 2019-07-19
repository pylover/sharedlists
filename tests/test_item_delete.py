from bddrest import status, response, when

from .conftest import RESTAPITestCase
from sharedlists.models import User, List, Item


class TestItemDelete(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        franz = User(id='franz', email='franz@example.com', password='12345')
        foo = List(title='foo')
        foo.items.append(Item(title='bar', owner=oscar.id))
        foo.items.append(Item(title='baz', owner=franz.id))
        oscar.lists.append(foo)
        session.add(oscar)
        session.add(franz)
        session.commit()

    def test_item_delete_anonymous(self):
        with self.given(
            'Delete an item from a list by anonymous',
            '/oscar/foo/bar',
            'DELETE',
        ):
            assert status == 401

    def test_item_delete(self):
        self.login('oscar', '12345')
        with self.given(
            'Delete an item from a list',
            '/oscar/foo/bar',
            'DELETE',
        ):
            assert status == 200
            assert response.text == \
f'''
Item: oscar/foo/bar
'''

            when(
                'Delete another\'s item',
                '/oscar/foo/baz',
            )
            assert status == 403

