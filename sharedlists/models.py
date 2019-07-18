import uuid

from restfulpy.orm import DeclarativeBase, Field, relationship, \
    TimestampMixin, ModifiedMixin
from sqlalchemy import Integer, Unicode, ForeignKey


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
        protected=True
    )

    def create_jwt_principal(self, session_id=None):
        if session_id is None:
            session_id = str(uuid.uuid4())

        return JWTPrincipal(dict(
            id=self.id,
            title=self.title,
            role=self.role,
            sessionId=session_id,
        ))

    def create_refresh_principal(self):
        return JWTRefreshToken(dict(
            id=self.id
        ))


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

