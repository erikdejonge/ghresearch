#!/usr/bin/env python3
# coding=utf-8
"""
Recursively generate an index of all the files in the specified folder

Usage:
  genindex.py [options] <folder>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : devenv
created : 19-05-15 / 15:12
"""
import os

from rst2md import rst2md
from arguments import Arguments
from mdcodeblockcorrect import correct_codeblocks


def main():
    """
    main
    """
    arguments = Arguments(__doc__)
    print(arguments)

    for r, drs, fs in os.walk(arguments.folder):
        for f in fs:
            tf = os.path.join(r, f)

            if tf.endswith("rst"):
                try:
                    rst2md(tf)
                    correct_codeblocks(tf.replace(".rst", ".md"))
                except UnicodeDecodeError:
                    print("error", tf)


    index = []

    for r, drs, fs in os.walk(arguments.folder):
        for f in fs:
            tf = os.path.join(r, f)

            if tf.endswith("md"):
                index.append(tf)

    index.sort()
    indexpath = os.path.join(arguments.folder, "index.md")
    indexfile = open(indexpath, "w")
    indexfile.write("# Index " + arguments.folder + "\n\n")

    for i in index:
        indexfile.write("* [" + i.replace(".md", "") + "](" + i.replace(".md", ".html") + ")\n")

    indexfile.close()


if __name__ == "__main__":
    main()
