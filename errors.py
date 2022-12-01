class InvalidShareParams(Exception):

    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(message, kwargs)


class InvalidPercentParams(Exception):
    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(message, kwargs)
