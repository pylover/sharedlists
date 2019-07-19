from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession

from .models import User


class Authenticator(StatefulAuthenticator):

    @staticmethod
    def safe_user_lookup(condition):
        user = DBSession.query(User).filter(condition).one_or_none()
        if user is None:
            raise HTTPStatus('400 Invalid request: not a user.')

        return user

    def create_principal(self, user_id=None, session_id=None):
        user = self.safe_user_lookup(User.id == user_id)
        principal = user.create_jwt_principal()
        return principal

    def create_refresh_principal(self, user_id=None):
        user = self.safe_user_lookup(User.id == user_id)
        return user.create_refresh_principal()

    def validate_credentials(self, credentials):
        email, password = credentials
        user = DBSession.query(User) \
            .filter(User.email == email) \
            .one_or_none()

        if user is None or not user.validate_password(password):
            return None

        return user

