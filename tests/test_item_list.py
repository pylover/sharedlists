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
        session.add(oscar)
        session.add(franz)
        session.commit()

    def test_item_list(self):
        with self.given('List items', '/oscar/foo'):
            assert status == 200
            assert response.text == \
f'''
bar
qux
baz
'''

            when('List detailed items', query='verbose=true')
            assert status == 200
            assert response.text == \
f'''
oscar\t\tbar
oscar\t\tqux
franz\t\tbaz
'''
