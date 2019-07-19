from bddrest import status, response

from .conftest import RESTAPITestCase
from sharedlists.models import User


class TestLogin(RESTAPITestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        oscar = User(
            id='oscar',
            email='oscar@example.com',
            password = 'password'
        )

        session.add(oscar)
        session.commit()

    def test_login(self):
        with self.given(
            'Logging-in',
            verb='LOGIN',
            form=dict(email='oscar@example.com', password='password')
        ):

            assert status == '200 OK'
            assert len(response.text.split('.')) == 3

