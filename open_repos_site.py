#!/usr/bin/env python3
# coding=utf-8
"""
Project ghresearch

Usage:
  open_repos_site.py [options] <input>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : ghresearch
created : 30 Oct 2016 / 16:56
where   : Latitude: 51.825426
          longitude: 4.650939
          https://www.google.nl/maps/place/51.825426,4.650939
"""
import os
import sys
import webbrowser

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
    config = os.path.join(os.getcwd(), arguments.input)
    origin = False
    for line in open(config):

        if line.strip().startswith("[remote"):
            origin = True


        elif origin:

            if line.strip().startswith("["):
                origin = False

            if line.strip().startswith("url"):
                burl = line.split(":")[0].split("@")[-1]
                url = line.split(":")[-1].strip().strip(".git")
                furl = "https://"+burl+"/"+url
                print(furl)
                webbrowser.open(furl)


if __name__ == "__main__":
    main()
