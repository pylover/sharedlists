from bddrest import status, response

from .conftest import RESTAPITestCase
from sharedlists.models import User, List, Item


class TestItemAdd(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(name='oscar', email='oscar@example.com', password='12345')
        foo = List(title='foo', author=oscar)
        session.add(foo)
        session.commit()

    def test_item_add_anonymous(self):
        with self.given(
            'Adding an item to a list by anonymous',
            '/lists/foo/bar',
            'ADD',
        ):
            assert status == 401


