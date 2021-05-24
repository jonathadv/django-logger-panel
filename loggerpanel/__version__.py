"""
Having a tuple like this makes it easy for other packages to compare versions, e.g.:
if VERSION > (3,):
if VERSION < (1, 8):
"""


VERSION = (0, 1, 1)

__version__ = ".".join(map(str, VERSION))
