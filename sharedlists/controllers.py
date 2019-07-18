from nanohttp import text
from restfulpy.controllers import RootController


CR = '\r\n'


class Root(RootController):

    @text
    def info(self):
        from sharedlists import __version__ as appversion
        return CR.join((
            f'Shared Lists v{appversion}',
            f'Total Lists: NaN',
            f'Total Members: NaN',
            ''
        ))


