from importlib.metadata import version

from .chart import Chart

__version__ = version("toga_chart")

__all__ = ["Chart"]
