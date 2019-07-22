
from .application import SharedLists
from .bee import Bee


__version__ = '0.3.0a2'


server_main = lambda: SharedLists().cli_main()
client_main = lambda: Bee().main()

