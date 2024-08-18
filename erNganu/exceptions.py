"""
Exceptions which can be raised by py-Ultroid Itself.
"""


class erNganuError(Exception):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(erNganuError):
    ...
