from bddrest import status, response, when

from .conftest import RESTAPITestCase
from sharedlists.models import User, Item


class TestItemList(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        franz = User(id='franz', email='franz@example.com', password='12345')
        oscar.items.append(Item(listowner=oscar, list='foo', title='bar'))
        franz.items.append(Item(listowner=oscar, list='foo', title='baz'))
        oscar.items.append(Item(listowner=oscar, list='foo', title='qux'))
        oscar.items.append(Item(listowner=franz, list='quux', title='quuz'))
        session.add(oscar)
        session.add(franz)
        session.commit()

    def test_item_list(self):
        with self.given('List items', '/oscar/foo'):
            assert status == 200
            assert response.text == \
f'''\
bar
qux
baz
'''
        self.login('oscar', '12345')
        with self.given('List all items', '/'):
            assert status == 200
            assert response.text == \
f'''\
franz/quux/quuz
oscar/foo/bar
oscar/foo/baz
oscar/foo/qux
'''

