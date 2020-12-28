from requests import Session


class BaseChecker:
    def __init__(self, address):
        self.session = Session()
        self.address = address

    def has_coverage(self):
        raise NotImplementedError('You must implement this method.')
