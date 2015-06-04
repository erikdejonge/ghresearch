# coding=utf-8
"""
convert rst file

Usage:
  mdcodeblockcorrect.py [options] <mdfile>

Options:
  -h --help     Show this screen.
  -v --verbose  Print arguments
  -f --force    Force check
  -s --silent   Folder from where to run the command [default: .].
"""
from arguments import Arguments
from consoleprinter import forceascii

import os


def correct_codeblocks(mdfile, force=False, fromsrt=False):
    """
    @type mdfile: str
    @return: None
    """
    try:
        inbuf = [x.rstrip().replace("\t", "    ") for x in open(mdfile)]
    except:
        inbuf = []

        for l in open(mdfile):
            inbuf.append(forceascii(l).replace("\t", "    "))

    outbuf = []
    cb = False
    inblock = False
    cnt = 0

    for l in inbuf:
        if "```" in l:
            if force is False:
                return 0

    for l in inbuf:
        if fromsrt:
            l = l.replace("###", "")

            if l.strip().startswith("`") and l.strip().endswith("`") and "```" not in l:
                l = l.replace("`", "##", 1).lstrip()
                l = l.replace("`", "")

            if "`" in l and l.count("`") != 3:
                l = l.replace("`", "")

            if l.strip().startswith("```"):
                if inblock:
                    inblock = False
                else:
                    inblock = True

            if not inblock:
                if not l.strip().startswith("-") and not l.strip().startswith("1") and not l.strip().startswith(">"):
                    if (l.strip().startswith("sed") or l.strip().startswith("gsed")) and not cb:
                        outbuf.append("\n```bash")
                        cnt += 1
                        cb = True
                    elif l.startswith("    ") and not l.strip().startswith("<") and not "/>" in l and not l.endswith(";") and not "`" in l and not cb:
                        if not cb:
                            cnt += 1
                            outbuf.append("\n```python")

                        cb = True
                    else:
                        if cb is True:
                            if not (l.strip().startswith("sed") or l.strip().startswith("gsed") or l.startswith("    ") or len(l.strip()) == 0):
                                cb = False
                                outbuf.append("```\n")

                if cb is True:
                    l = l.replace("    ", "", 1)

        outbuf.append(l)

    if cb is True:
        outbuf.append("```")

    outbuf = "\n".join(outbuf)

    if force is True:
        outbuf = outbuf.replace("```", "\n```")
        outbuf = outbuf.replace("\n\n\n```", "\n\n```")
        outbuf = outbuf.replace("```\n\n```", "")
        outbuf = outbuf.replace("```\n\n python\n", "\n\n``` python\n")
        outbuf = outbuf.replace("```\n\n bash\n", "\n\n``` bash\n")
        outbuf = outbuf.replace("-   [", "- [")
        outbuf = outbuf.replace("-   ", "- ")
        outbuf = outbuf.replace("1.   ", "1. ")
        outbuf = outbuf.replace("\n\n\n", "\n\n")
    open(mdfile, "w").write(outbuf)
    return cnt


def main():
    """
    main
    """
    arg = Arguments(doc=__doc__)
    if arg.verbose is True:
        print(arg)
    if arg.mdfile.lower().strip().endswith(".markdown"):
        print("mv " + arg.mdfile + " " + arg.mdfile.replace(".markdown", ".md"))
        os.system("mv " + arg.mdfile + " " + arg.mdfile.replace(".markdown", ".md"))
    if not os.path.exists(arg.mdfile):
        print("file does not exist")
        return

    mdfile = arg.mdfile
    cnt = correct_codeblocks(mdfile, arg.force)
    if not arg.silent:
        if cnt != 0:
            print("\033[34m" + arg.mdfile.lower(), "->\033[0;96m " + str(cnt) + " code blocks corrected\033[0m")


if __name__ == "__main__":
    main()
