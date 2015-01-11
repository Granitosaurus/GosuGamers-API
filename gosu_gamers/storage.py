import json


class Storage:
    """
    Storage meta class for storage items such as match, team, player etc.
    """

    def get_json(self):
        return json.dumps(self.__dict__())

    def get_dict(self):
        return self.__dict__()