# coding=utf-8
"""
Lorum ipsum

Usage:
  keeponlyreadmes [options] <target_dir>

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : ghresearch
created : 21-05-15 / 22:12
"""
from arguments import Arguments

import os


class IArguments(Arguments):
    """
    IArguments
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
        self.help = False
        self.target_dir = ""
        super().__init__(doc, validateschema, argvalue, yamlstr, yamlfile, parse_arguments, persistoption, alwaysfullhelp, version, parent)


def main():
    """
    main
    """
    arg = Arguments(__doc__)
    print(arg.get_subclass())
    bs = arg.target_dir
    for d in os.listdir(bs):

        fp = os.path.join(bs, d)
        rm = os.path.join(fp, "readme.md")
        np = os.path.expanduser("~/workspace/markdown-to-ebook/bookcvwait/githubreadme/") + d + "/readme.md"

        if not os.path.exists(rm):
            rm = os.path.join(fp, "readme.rst")
            np = os.path.expanduser("~/workspace/markdown-to-ebook/bookcvwait/githubreadme/") + d + "/readme.rst"

        if os.path.exists(rm):
            c = open(rm).read()
            print("\033[94m>", rm ,"\033[0m")

            os.makedirs(os.path.dirname(np), exist_ok=True)
            open(np, "w").write(c)
            pass

    for r, ds, f in os.walk(arg.target_dir):
        if r != arg.target_dir and os.path.dirname(r) == arg.target_dir:
            if len(f) == 0 and len(ds) == 0:
                os.rmdir(r)
            elif len(ds) == 0:
                printf = True

                for fw in f:
                    if not fw.startswith("."):
                        printf = False

                if printf:
                    for fw in f:
                        os.remove(os.path.join(r, fw))

                    os.rmdir(r)


if __name__ == "__main__":
    main()
