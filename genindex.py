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


class IArgument(Arguments):
    """
    IArgument
    """
    def __init__(self, doc=None, validateschema=None, argvalue=None, yamlstr=None, yamlfile=None, parse_arguments=True, persistoption=False, alwaysfullhelp=False, version=None, parent=None):
        """
        @type doc: str, None
        @type validateschema: Schema, None
        @type yamlfile: str, None
        @type yamlstr: str, None
        @type parse_arguments: bool
        @type argvalue: str, None
        @return: None
        """
        self.folder = ""
        self.help = False
        super().__init__(doc, validateschema, argvalue, yamlstr, yamlfile, parse_arguments, persistoption, alwaysfullhelp, version, parent)


def main():
    """
    main
    """
    arguments = IArgument(__doc__)
    for r, drs, fs in os.walk(arguments.folder):
        if str(r.strip().strip("/")).endswith("docs"):
            mk = os.path.join(r, "Makefile")
            if os.path.exists(mk):
                currd = os.getcwd()
                os.chdir(r)
                os.system("make html")
                os.system("find . -type f -name '*.rst' -ls -delete")
                os.system("rm Makefile")
                os.chdir(currd)


    for r, drs, fs in os.walk(arguments.folder):
        for f in fs:
            tf = os.path.join(r, f)

            if tf.endswith("rst"):
                try:
                    rst2md(tf)
                    correct_codeblocks(tf.replace(".rst", ".md"), True)
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
        if "source/api" not in i:
            if i.lower().endswith("readme.md"):
                indexfile.write("* [*" + os.path.dirname(i).replace(arguments.folder, "") + "/" + os.path.basename(os.path.dirname(i)) + "/" + os.path.basename(i).replace(".md", "") + "*](" + i.replace(".md", ".html").replace(arguments.folder, ".") + ")\n")
            else:
                indexfile.write("* [" + i.replace(".md", "").replace(os.path.dirname(arguments.folder), "") + "](" + i.replace(".md", ".html").replace(arguments.folder, ".") + ")\n")

    indexfile.close()


if __name__ == "__main__":
    main()
