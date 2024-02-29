"""
classes to log custom exceptions
"""


class Exceptions(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidDataException(Exceptions):
    def __init__(self, *args):
        super().__init__(*args)


class NetworkError(Exceptions):
    def __init__(self, *args):
        super().__init__(*args)
