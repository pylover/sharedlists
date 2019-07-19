from bddrest import status, response

from sharedlists import __version__ as appversion
from sharedlists.models import User, List

from .conftest import RESTAPITestCase


class TestLogin(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        oscar = User(
            name='oscar',
            email='oscar@example.com',
            password = 'password'
        )

        foo = List(title='Foo', author=oscar)
        session.add(foo)
        session.commit()

    def test_login(self):
        with self.given(
            'Logging-in',
            verb='LOGIN',
            form=dict(email='oscar@example.com', password='password')
        ):

            assert status == '200 OK'
            assert len(response.text.split('.')) == 3

