from os.path import dirname

from restfulpy import Application

from .controllers import Root
from .authentication import Authenticator


class SharedLists(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''
      db:
        url: postgresql://postgres:postgres@localhost/sharelists_dev
        test_url: postgresql://postgres:postgres@localhost/sharelists_test
        administrative_url: postgresql://postgres:postgres@localhost/postgres

      migration:
        directory: %(root_path)s/migration
        ini: %(root_path)s/alembic.ini

    '''

    def __init__(self, application_name='sharelists'):
        from sharedlists import __version__
        super().__init__(
            application_name,
            root=Root(),
            root_path=dirname(__file__),
            version=__version__
        )

    def insert_mockup(self, args):
        from restfulpy.orm import DBSession
        from .models import User
        oscar = User(id='pylover', email='pylover@example.com', password='12345')
        DBSession.add(oscar)
        DBSession.commit()

