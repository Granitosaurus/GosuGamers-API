import json


class Storage:
    """
    Storage meta class for storage items such as match, team, player etc.
    """

    @property
    def json(self):
        return json.dumps(self.__dict__())

    @property
    def dictionary(self):
        return self.__dict__()