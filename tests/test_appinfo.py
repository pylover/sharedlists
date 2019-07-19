from bddrest import status, response

from sharedlists import __version__ as appversion
from sharedlists.models import User, List

from .conftest import RESTAPITestCase


class TestApplicationInfo(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        oscar = User(name='oscar', email='oscar@example.com', password='12345')
        foo = List(title='Foo', author=oscar)
        session.add(foo)
        session.commit()

    def test_info_anonymous(self):
        with self.given(
            'Getting the application information by an anonymous',
            verb='INFO'
        ):
            assert status == '200 OK'
            assert response.text == \
f'''
Shared Lists v{appversion}
Total Lists: 1
Total Users: 1
'''

    def test_info_authenticated(self):
        self.login('oscar@example.com', '12345')
        with self.given(
            'Getting the application information by an authenticated user',
            verb='INFO'
        ):

            assert status == '200 OK'
            assert response.text == \
f'''
Shared Lists v{appversion}
Total Lists: 1
Total Users: 1
My Lists: 1
'''

