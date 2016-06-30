from __future__ import absolute_import, unicode_literals

from itertools import groupby


class Command:
    """
    A Command represents an operation that has to be executed
    on a block for it to be converted into an arbitrary number
    of HTML nodes.
    """
    def __init__(self, name, index, data=''):
        self.name = name
        self.index = index
        self.data = data

    def __str__(self):
        return '<Command {0} {1} {2}>'.format(self.name, self.index, self.data)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.index < other.index

    @staticmethod
    def key(command):
        return command.index

    @staticmethod
    def grouped_by_index(commands):
        return groupby(sorted(commands), Command.key)

    @staticmethod
    def start_stop(name, start, stop, data=''):
        """
        Builds a pair of start/stop commands with the same data.
        """
        return [
            Command('start_%s' % name, start, data),
            Command('stop_%s' % name, stop, data),
        ]

    @staticmethod
    def from_ranges(ranges, name, data_key, start_key='offset', length_key='length'):
        """
        Creates a list of commands from a list of ranges. Each range
        is converted to two commands: a start_* and a stop_*.
        """
        commands = []
        for r in ranges:
            data = r.get(data_key)
            start = r.get(start_key)
            stop = start + r.get(length_key)
            commands.extend(Command.start_stop(name, start, stop, data))
        return commands
