

#class Authenticator(StatefulAuthenticator):
#
#    @staticmethod
#    def safe_member_lookup(condition):
#        member = DBSession.query(Member).filter(condition).one_or_none()
#        if member is None:
#            raise HTTPStatus('400 Incorrect Email Or Password')
#
#        return member
#
#    def create_principal(self, member_id=None, session_id=None):
#        member = self.safe_member_lookup(Member.id == member_id)
#        principal = member.create_jwt_principal()
#
#        payload = self.get_previous_payload()
#        payload.update(principal.payload)
#        principal.payload = payload
#
#        return principal
#
#    def create_refresh_principal(self, member_id=None):
#        member = self.safe_member_lookup(Member.id == member_id)
#        return member.create_refresh_principal()
#
#    def validate_credentials(self, email):
#        member = self.safe_member_lookup(Member.email == email)
#        return member
#
#    def verify_token(self, encoded_token):
#        principal = CASPrincipal.load(encoded_token)
#
#        member = DBSession.query(Member) \
#            .filter(Member.reference_id == principal.reference_id) \
#            .one_or_none()
#        if not member:
#            raise HTTPUnauthorized()
#
#        cas_member = CASClient().get_member(member.access_token)
#
#        self.update_member_if_needed(member, cas_member)
#        return principal
#
#    def update_member_if_needed(self, member, cas_member):
#
#        # FIXME: If any item added to scopes, the additional scopes item must
#        # be considered here
#        if member.title != cas_member['title']:
#            member.title = cas_member['title']
#
#        if member.avatar != cas_member['avatar']:
#            member.avatar = cas_member['avatar']
#
#        if member.name != cas_member['name']:
#            member.name = cas_member['name']
#
#        DBSession.commit()
#
#    def get_previous_payload(self):
#        if hasattr(context, 'identity') and context.identity:
#            return context.identity.payload
#
#        if 'HTTP_AUTHORIZATION' in context.environ:
#            token = context.environ['HTTP_AUTHORIZATION']
#            token = token.split(' ')[1] if token.startswith('Bearer') else token
#
#            jsonWebSerializer = JSONWebSignatureSerializer('secret')
#            payload = jsonWebSerializer.loads_unsafe(token)
#            return payload[1]
#
#        return {}
#
