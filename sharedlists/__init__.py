
from .application import SharedLists
from .bee import Bee


__version__ = '1.2.0'


server_main = lambda: SharedLists().cli_main()
client_main = lambda: Bee().main()

