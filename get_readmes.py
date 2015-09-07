#!/usr/bin/env python3
# coding=utf-8
"""
Get readmes

Usage:
  get_readmes.py [options] [--] <target_dir>

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


def check_folder(bs):
    """
    @type bs: list
    @return: None
    """
    for d in os.listdir(bs):
        fp = os.path.join(bs, d)
        rm = os.path.join(fp, "readme.md")
        np = "./githubreadme" + "/" + d + "/readme.md"

        if os.path.exists(rm):
            c = open(rm).read()
            print(os.path.abspath(os.path.dirname(np)), np, len(c))
            os.makedirs(os.path.dirname(np), exist_ok=True)
            open(np, "w").write(c)
            pass


def main():
    """
    main
    """
    arg = arguments.Arguments(__doc__)
    targetdir = os.path.expanduser(arg.target_dir)

    if targetdir == ".":
        targetdir = os.getcwd()

    outdir = os.getcwd()

    #os.system("rm -Rf "+os.path.join(outdir, "githubreadme")+"/*")
    targetdir = os.path.expanduser(targetdir)
    os.chdir(targetdir)
    check_folder(targetdir)


if __name__ == "__main__":
    main()
