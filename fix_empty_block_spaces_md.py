#!/usr/bin/env python3
# coding=utf-8
"""
Project ghresearch

Usage:
  fix_empty_block_spaces_md.py [options] <input>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : ghresearch
created : 30 Oct 2016 / 17:47
where   : Latitude: 51.825435
          longitude: 4.650934
          https://www.google.nl/maps/place/51.825435,4.650934
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
    inblock = False
    newfile = ""
    for line  in open(arguments.input):
        addline = True
        if inblock and line.startswith("```"):
            inblock = False
        elif line.startswith("```"):
            inblock = True
        if inblock and len(line.strip())==0:
            addline = False
        else:
            addline = True
        if addline:
            newfile += line
    open(arguments.input, "w").write(newfile)

if __name__ == "__main__":
    main()
