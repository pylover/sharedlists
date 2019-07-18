from bddrest import status, response

from sharedlists import __version__ as appversion
from .helpers import RESTAPITestCase


class TestApplicationInfo(RESTAPITestCase):

    def test_info(self):
        with self.given(
            'Getting the application information',
            '/info'
        ):
            assert status == '200 OK'
            assert response.text == f'Shared Lists v{appversion}\r\n' \
                'Total Lists: NaN\r\n' \
                'Total Members: NaN\r\n'



