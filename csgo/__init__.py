__version__ = "0.2.1"
__author__ = "Rossen Georgiev"

version_info = (0, 2, 1)


# proxy object
# avoids importing csgo.enums unless it's needed
class CSGOClient(object):
    def __new__(cls, *args, **kwargs):
        from csgo.client import CSGOClient as CSC
        return CSC(*args, **kwargs)

import sharecode
