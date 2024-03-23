from enum import StrEnum

class UnderscoreEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        _name = name.removeprefix('_')
        _name = _name.replace('__', '/')
        _name = _name.replace('_', '.')
        return _name