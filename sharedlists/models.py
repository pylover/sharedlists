import os
import uuid
from _sha256 import sha256

from sqlalchemy import Integer, Unicode, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint
from sqlalchemy.orm import synonym
from nanohttp import context
from restfulpy.orm import DeclarativeBase, Field, relationship, \
    TimestampMixin, ModifiedMixin
from restfulpy.principal import JWTPrincipal, JWTRefreshToken


USER_NAME_SQLTYPE = Unicode(16)
LIST_TITLE_SQLTYPE = Unicode(50)
ITEM_TITLE_SQLTYPE = Unicode(50)


class User(TimestampMixin, DeclarativeBase):
    __tablename__ = 'user'

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

    id = Field(
        USER_NAME_SQLTYPE,
        not_none=True,
        required=True,
        primary_key=True
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

    title = Field(
        LIST_TITLE_SQLTYPE,
        not_none=True,
        required=True,
        index=True,
        primary_key=True
    )

    owner = Field(ForeignKey('user.id'), primary_key=True)

    items = relationship(
        'Item',
        lazy='dynamic',
        protected=True
    )

    @property
    def fulltitle(self):
        return f'{self.owner}/{self.title}'

    def __str__(self):
        return \
f'''
List: {self.fulltitle}
'''


class Item(ModifiedMixin, DeclarativeBase):
    __tablename__ = 'item'

    id = Field(Integer, primary_key=True)
    title = Field(
        ITEM_TITLE_SQLTYPE,
        not_none=True,
        required=True,
    )

    owner = Field(USER_NAME_SQLTYPE)
    list = Field(LIST_TITLE_SQLTYPE)

    __table_args__ = (
        UniqueConstraint(
            owner, list, title,
            name='uix_owner_list_title'
        ),
        ForeignKeyConstraint(
            [owner, list],
            [List.owner, List.title],
        ),
    )

    @property
    def fulltitle(self):
        return f'{self.owner}/{self.list}/{self.title}'

    def __str__(self):
        return \
f'''
Item: {self.fulltitle}
'''


