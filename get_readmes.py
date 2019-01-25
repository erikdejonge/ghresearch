#!/usr/bin/env python3
# coding=utf-8
"""
Get readmes

Usage:
  get_readmes.py [options] [--] <source_dir> <target_dir>

Options:
  -h --help     Show this screen.

Description:
target_dir   Folder to check

Active8 (18-05-15)
author: erik@a8.nl
license
"""
import os
import arguments


def check_folder(bs, td):
    """
    @type bs: list
    @return: None
    """

    for d in os.listdir(bs):

        fp = os.path.join(bs, d)
        rm = os.path.join(fp, "readme.md")
        np = os.path.join(td, "githubreadme" + "/" + d + "/readme.md")

        if os.path.exists(rm):
            c = open(rm).read()
            os.makedirs(os.path.dirname(np), exist_ok=True)
            with open(np, "w") as fout:
                fout.write(c)

        else:
            if os.path.isdir(fp):
                check_folder(fp, td)
                print('check_folder', fp, td)

def ossystem(cmd):
    """
    @type cmd: str
    @return: None
    """
    print(cmd)
    os.system(cmd)


def main():
    """
    main
    """
    arg = arguments.Arguments(__doc__)
    print(arg)
    sourcedir = os.path.expanduser(arg.source_dir)
    targetdir = os.path.expanduser(arg.target_dir)

    print(sourcedir)
    print(targetdir)

    os.system("rm -Rf " + targetdir)
    targetdir = os.path.expanduser(targetdir)
    os.chdir(sourcedir)
    check_folder(sourcedir, targetdir)
    #ossystem("mv " + sourcedir + " " + os.path.join(arg.target_dir, "githubreadme"))
    #os.chdir(os.path.join(arg.target_dir, "githubreadme"))


if __name__ == "__main__":
    main()
