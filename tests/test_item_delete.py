from bddrest import status, response, when

from .conftest import RESTAPITestCase
from sharedlists.models import User, Item


class TestItemDelete(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(id='oscar', email='oscar@example.com', password='12345')
        franz = User(id='franz', email='franz@example.com', password='12345')
        oscar.items.append(Item(listowner=oscar, list='foo', title='bar'))
        franz.items.append(Item(listowner=oscar, list='foo', title='baz'))
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
oscar/foo/bar
'''

            when('Delete the item again')
            assert status == 404

            when('Delete another\'s item', '/oscar/foo/baz')
            assert status == 403

