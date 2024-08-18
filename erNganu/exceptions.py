"""
Exceptions which can be raised by er-Nganu Itself.
"""


class erNganuError(Exception):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(erNganuError):
    ...
