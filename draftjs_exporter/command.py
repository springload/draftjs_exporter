from typing import Any, List, Mapping, Sequence, Tuple, Union


class Command(object):
    """
    A Command represents an operation that has to be executed
    on a block for it to be converted into an arbitrary number
    of HTML nodes.
    """
    __slots__ = ('name', 'index', 'data')

    def __init__(self, name: str, index: int, data: str = '') -> None:
        self.name = name
        self.index = index
        self.data = data

    def __str__(self) -> str:
        return '<Command {0} {1} {2}>'.format(self.name, self.index, self.data)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def start_stop(name: str, start: int, stop: int, data: str = '') -> Tuple['Command', 'Command']:
        """
        Builds a pair of start/stop commands with the same data.
        """
        return (
            Command('start_%s' % name, start, data),
            Command('stop_%s' % name, stop, data),
        )

    @staticmethod
    def from_ranges(ranges: Sequence[Mapping[str, Any]], name: str, data_key: str) -> List['Command']:
        """
        Creates a list of commands from a list of ranges. Each range
        is converted to two commands: a start_* and a stop_*.
        """
        commands = []  # type: List['Command']
        for r in ranges:
            data = r[data_key]
            start = r['offset']
            stop = start + r['length']
            commands.extend(Command.start_stop(name, start, stop, data))
        return commands
