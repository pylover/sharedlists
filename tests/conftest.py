from os import path

from restfulpy.testing import ApplicableTestCase
from restfulpy.principal import JWTPrincipal

from sharedlists import SharedLists
from sharedlists.models import User


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class RESTAPITestCase(ApplicableTestCase):
    __application__ = SharedLists()
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __metadata__ = {
        #r'^/lists.*': List.json_metadata()['fields']
    }

    def login(self, email):
        user = self._session.query(User).filter(User.email == email) \
            .one_or_none()

        if user is None:
            raise ValueError(f'User not Found: {email}')

        principal = user.create_jwt_principal()
        token = principal.dump()
        self._authentication_token = token.decode('utf-8')

