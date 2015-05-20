# coding=utf-8
"""
devenv/testmdcheck
-

Active8 (07-05-15)
author: erik@a8.nl
license: GNU-GPL2
"""
import os
import shutil
import mdcodeblockcorrect


def main():
    """
    main
    """
    shutil.copy2("./test/bronrst.txt", "./test/testfile.rst")
    os.system("python3 ~/workspace/devenv/rst2md.py -f ./test/testfile.rst")
    os.system("python3 ~/workspace/devenv/mdcodeblockcorrect.py ./test/testfile.md")


if __name__ == "__main__":
    main()
