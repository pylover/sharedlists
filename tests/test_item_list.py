from bddrest import status, response, when

from .conftest import RESTAPITestCase
from sharedlists.models import User, List, Item


class TestItemList(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        franz = User(id='franz', email='franz@example.com', password='12345')
        foo = List(title='foo')
        foo.items.append(Item(title='bar', owner=oscar.id))
        foo.items.append(Item(title='baz', owner=franz.id))
        foo.items.append(Item(title='qux', owner=oscar.id))
        oscar.lists.append(foo)
        session.add(oscar)
        session.add(franz)
        session.commit()

    def test_item_list(self):
        with self.given(
            'Delete an item from a list by anonymous',
            '/oscar/foo',
        ):
            assert status == 200
            assert response.text == \
f'''
bar
baz
qux
'''

            when(
                'Delete another\'s item',
                query='verbose=true'
            )
            assert status == 200
            assert response.text == \
f'''
oscar\t\tbar
franz\t\tbaz
oscar\t\tqux
'''
