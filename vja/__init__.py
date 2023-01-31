__all__ = ['apiclient', 'service', 'config', 'login', 'VjaError']


class VjaError(Exception):
    """Internal error"""

    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return 'VjaError("%s")' % self.msg

    def __str__(self):
        return self.msg
