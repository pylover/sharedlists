from bddrest import status, response

from .conftest import RESTAPITestCase
from sharedlists.models import User, List, Item


class TestItemAdd(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        oscar.lists.append(List(title='foo'))
        session.add(oscar)
        session.commit()

    def test_item_add_anonymous(self):
        with self.given(
            'Adding an item to a list by anonymous',
            '/oscar/foo/bar',
            'APPEND',
        ):
            assert status == 401

    def test_item_add(self):
        self.login('oscar', '12345')
        with self.given(
            'Adding an item to a list by anonymous',
            '/oscar/foo/bar',
            'APPEND',
        ):
            assert status == 200
            assert response.text == \
f'''
Item: oscar/foo/bar
'''


