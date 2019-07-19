import os
import uuid
from _sha256 import sha256

from sqlalchemy import Integer, Unicode, ForeignKey
from sqlalchemy.orm import synonym
from nanohttp import context
from restfulpy.orm import DeclarativeBase, Field, relationship, \
    TimestampMixin, ModifiedMixin
from restfulpy.principal import JWTPrincipal, JWTRefreshToken


class User(TimestampMixin, DeclarativeBase):
    __tablename__ = 'user'

    id = Field(
        Integer,
        primary_key=True,
        readonly=True,
        not_none=True,
        required=False,
        label='ID',
        minimum=1,
        example=1,
        protected=False,
    )
    email = Field(
        Unicode(100),
        index=True,
        unique=True,

        not_none=True,
        required=True,
        python_type=str,
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        pattern_description='Invalid email format, example: user@example.com',
        example='user@example.com',
        label='Email',
    )

    name = Field(
        Unicode(16),
        not_none=True,
        required=True,
        unique=True,
    )

    role = Field(
        Unicode(16),
        readonly=True,
        not_none=True,
        required=False,
        default='user',
    )

    lists = relationship(
        'List',
        back_populates='author',
        lazy='dynamic',
        protected=True
    )

    _password = Field(
        'password',
        Unicode(128),
        index=True,
        protected=True,
    )

    @property
    def roles(self):
        return ['member']

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym(
        '_password',
        descriptor=property(_get_password, _set_password),
        info=dict(protected=True)
    )

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hashed_pass = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hashed_pass.update((password + salt).encode('utf-8'))
        hashed_pass = hashed_pass.hexdigest()

        password = salt + hashed_pass
        return password

    def validate_password(self, password):
        """
        Check the password against existing credentials.
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool
        """
        hashed_pass = sha256()
        hashed_pass.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hashed_pass.hexdigest()

    def create_jwt_principal(self, session_id=None):
        if session_id is None:
            session_id = str(uuid.uuid4())

        return JWTPrincipal(dict(
            id=self.id,
            name=self.name,
            role=self.role,
            sessionId=session_id,
        ))

    def create_refresh_principal(self):
        return JWTRefreshToken(dict(
            id=self.id
        ))

    @classmethod
    def get_current(cls, session):
        if not hasattr(context, 'identity') or context.identity is None:
            return None

        principal = context.identity
        return session.query(cls) \
            .filter(cls.id == principal.payload.get('id')) \
            .one_or_none()


class List(ModifiedMixin, DeclarativeBase):
    __tablename__ = 'list'

    id = Field(
        Integer,
        primary_key=True,
        readonly=True,
        not_none=True,
        required=False,
        label='ID',
        minimum=1,
        example=1,
        protected=False,
    )
    title = Field(
        Unicode(50),
        unique=True,
        not_none=True,
        required=True,
        index=True,
    )

    author_id = Field(ForeignKey('user.id'))
    author = relationship('User', back_populates='lists')

    def __str__(self):
        return \
f'''
List: {self.title}
'''
