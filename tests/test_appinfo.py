from bddrest import status, response

from sharedlists import __version__ as appversion
from sharedlists.models import User, List

from .conftest import RESTAPITestCase


class TestApplicationInfo(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(name='oscar', email='oscar@example.com')
        foo = List(title='Foo', author=oscar)
        session.add(foo)
        session.commit()

    def test_info(self):
        with self.given(
            'Getting the application information',
            '/info'
        ):
            assert status == '200 OK'
            assert response.text == f'Shared Lists v{appversion}\r\n' \
                'Total Lists: 1\r\n' \
                'Total Users: 1\r\n'



