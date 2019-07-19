from bddrest import status, response

from sharedlists import __version__ as appversion
from sharedlists.models import User, List

from .conftest import RESTAPITestCase


class TestListCreate(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(name='oscar', email='oscar@example.com', password='12345')
        session.add(oscar)
        session.commit()

    def test_list_create_anonymous(self):
        with self.given(
            'Creating list by an anonymous',
            '/lists',
            'CREATE',
            form=dict(title='foo')
        ):
            assert status == 401

    def test_list_create_authenticated(self):
        self.login('oscar@example.com', '12345')
        with self.given(
            'Creating list by an anonymous',
            '/lists',
            'CREATE',
            form=dict(title='foo')
        ):
            assert status == '200 OK'
            assert response.text == f''


