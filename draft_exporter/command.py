class Command:
    def __init__(self, name, index, data=''):
        self.name = name
        self.index = index
        self.data = data

    def __str__(self):
        return '<Command {0} {1} {2}>'.format(self.name, self.index, self.data)
