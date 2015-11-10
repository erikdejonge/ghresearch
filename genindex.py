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
                os.system("git reset --hard")
                if os.path.exists("requirements.txt"):
                    os.system("pip3 install -r requirements.txt")

                os.system("python3 setup.py install")
                currd = os.getcwd()
                os.chdir(r)
                os.system("make html")
                os.system("find . -type f -name '*.rst' -ls -delete")
                os.system("rm Makefile")

                os.chdir(currd)

    print(str(arguments.folder))

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
        tf = os.path.join(r, f)

        for f in fs:
            tf = os.path.join(r, f)

            if tf.strip().endswith("md"):
                index.append(tf)

    index.sort()
    indexpath = os.path.join(arguments.folder, "index.md")
    #indexfile = open(indexpath.replace(".html", ".md"), "w")
    indexfilebook = open(os.path.basename(arguments.folder) + ".md", "w")
    #indexfile.write("# Index " + os.path.basename(arguments.folder) + "\n\n")
    indexfilebook.write("# Index " + os.path.basename(arguments.folder) + "\n\n")
    cnt = 1

    chapters = {}
    chapters[os.path.basename(os.getcwd()).capitalize()] = []
    for i in index:
        if "source/api" not in i and "index" not in i and os.path.basename(arguments.folder) + ".md" not in i:
            #indexfile.write(str(cnt) + ". [" + i.replace(".md", "").replace(arguments.folder, "").replace("_", " ").strip('//').capitalize() + "](" + i.replace(arguments.folder.replace(".html", ".md"), ".") + ")\n")
            name = i.replace(".md", "").replace(arguments.folder, "").replace("_", " ").strip('//').capitalize()

            if "/" in name:
                name = name.split("/", 1)
                if name[0] not in chapters:
                    chapters[name[0]] = [(name[1].capitalize(), i)]
                else:
                    chapters[name[0]].append((name[1].capitalize(), i))
            else:

                chapters[os.path.basename(os.getcwd()).capitalize()].append((name, i))

    chapterkeys = list(chapters.keys())
    chapterkeys.sort()
    for chap in chapterkeys:
        if len(chapters[chap]) > 0:
            indexfilebook.write("\n\n## "+chap+"\n\n")
        chaps = sorted(chapters[chap], key=lambda x: x[0]+x[1])
        for name,i  in chaps:
            #print(name, i)
            indexfilebook.write(str(cnt) + ". [" + name + "](" + i.replace(".html", ".md").replace(arguments.folder, ".") + ")\n")
            cnt += 1

    #indexfile.close()
    indexfilebook.close()


if __name__ == "__main__":
    main()
