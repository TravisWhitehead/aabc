def connected(function):
    """
    Decorator that checks the gpapi status before doing any request
    """
    def check_connection(self, *args, **kwargs):
        if self.gpapi is None or self.gpapi.authSubToken is None:
            ok, err = self.connect()
            if not ok:
                exit(err)
        return function(self, *args, **kwargs)
    return check_connection
