import json
import pkg_resources


class Storage:
    """
    Storage meta class for storage items such as match, team, player etc.
    """

    known_params = {}
    schema_name = 'team'

    def __init__(self):
        self.schema = self.read_schema()
        self.known_params = self.schema['parameters']

    def read_schema(self):
        data = pkg_resources.resource_string('gosu_gamers', 'schema/{}.json'.format(self.schema_name))
        return json.loads(data.decode('utf-8'))[self.schema_name]

    def fill_details(self, override_all=False):
        """Fills up details if Team object has an ID does not fill up self.rank_change"""
        check = lambda element: (not element) or override_all
        # First no connection fields
        for param, value in self.known_params.items():
            if not check(getattr(self, param, value['default'])) or value.get('requires_connection', True):
                continue
            getter = getattr(self, 'get_{}'.format(param))
            setattr(self, param, getter())
        # Then connection requiring fields
        for param, value in self.known_params.items():
            if not check(getattr(self, param, value['default'])):
                continue
            getter = getattr(self, 'get_{}'.format(param))
            setattr(self, param, getter())

    @property
    def json(self):
        return json.dumps(self.__dict__())

    @property
    def dictionary(self):
        return self.__dict__()

if __name__ == '__main__':
    s = Storage()
    print(s.known_params)
