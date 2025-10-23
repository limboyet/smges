class AppErrorBaseClass(Exception):
    pass

class ObjectNotFound(AppErrorBaseClass):
    pass

class BadObjectRequest(AppErrorBaseClass):
    pass

class InvalidLogin(AppErrorBaseClass):
    pass

class InvalidToken(AppErrorBaseClass):
    pass

class DBConnection(AppErrorBaseClass):
    pass
