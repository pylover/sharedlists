from bddrest import status, response, when

from .conftest import RESTAPITestCase
from sharedlists.models import User, Item


class TestListList(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        franz = User(id='franz', email='franz@example.com', password='12345')
        oscar.items.append(Item(listowner=oscar, list='foo', title='bar'))
        franz.items.append(Item(listowner=oscar, list='foo', title='baz'))
        oscar.items.append(Item(listowner=oscar, list='quux', title='qux'))
        session.add(oscar)
        session.add(franz)
        session.commit()

    def test_list_list(self):
        with self.given('List lists', '/oscar'):
            assert status == 200
            assert response.text == \
f'''\
(2)\t\tfoo
(1)\t\tquux
'''


class TestListEmptyList(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        session.add(oscar)
        session.commit()

    def test_list_emptylist(self):
        with self.given('List lists', '/oscar'):
            assert status == 200
            assert response.text == ''
