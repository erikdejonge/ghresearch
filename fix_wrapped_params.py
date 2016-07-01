#!/usr/bin/env python3
# coding=utf-8
"""
Project markdown

Usage:
  fix_wrapped_params.py [options] <file>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : markdown
created : 28 Jun 2016 / 16:08
where   : Latitude: 51.957242
          longitude: 4.569463
          https://www.google.nl/maps/place/51.957242,4.569463
"""
import sys

from arguments import Arguments
from consoleprinter import console

if sys.version_info.major < 3:
    console("Python 3 is required", color="red", plaintext="True")
    exit(1)


class IArguments(Arguments):
    """
    IArguments
    """

    def __init__(self, doc):
        """
        __init__
        """
        self.help = False
        self.input = ""
        super().__init__(doc)


def main():
    """
    main
    """
    arguments = IArguments(__doc__)
    c = open(arguments.file).read()
    #print({1:c})

    for i in range(0, 20):
        rs = "\n"+(19-i)*' '+"\n"

        c = c.replace(rs, "*--*")
    c = c.replace("\n", " ")
    c = c.replace("`,", "`")
    c = c.replace("##", "#")
    c = c.replace("     ", "\n    ")

    c = c.replace("*--*", "\n\n")
    print(c)

if __name__ == "__main__":
    main()
