import os

def use(*args):
    global _stylesheet

    if len(args) > 0:
        _stylesheet = args[0]
