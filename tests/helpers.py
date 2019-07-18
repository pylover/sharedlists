from os import path

from restfulpy.testing import ApplicableTestCase

from sharedlists import SharedLists


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class RESTAPITestCase(ApplicableTestCase):
    __application__ = SharedLists()
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __metadata__ = {
        #r'^/lists.*': List.json_metadata()['fields']
    }

    def login(self, email, organization_id=None):
        session = self.create_session()
        member = session.query(Member).filter(Member.email == email) \
            .one_or_none()

        if member is None:
            raise ValueError(f'Member not Found: {email}')

        principal = member.create_jwt_principal()
        token = principal.dump()
        self._authentication_token = token.decode('utf-8')

