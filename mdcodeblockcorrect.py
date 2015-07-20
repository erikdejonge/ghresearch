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
    ismd = mdfile.strip().endswith("md")
    if force is True:
        if fromsrt is False:
            fromsrt = force
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
            if not ismd:
                l = l.replace("###", "")


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
                    elif (l.startswith("    ") or l.startswith("\t"))and not l.strip().startswith("<") and not "/>" in l and not l.endswith(";") and not "`" in l and not cb:
                        cnt += 1
                        if l.strip().startswith("$"):
                            outbuf.append("\n``` bash")
                        else:
                            outbuf.append("\n``` python")

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
        outbuf = outbuf.replace("\[", "[")
        outbuf = outbuf.replace("\]", "]")
        outbuf = outbuf.replace("\n\n\n", "\n\n")
        outbuf = outbuf.replace("programlisting", "python")
        outbuf = outbuf.replace("![](2.%20Why%20Value%20Matters%20Less%20with%20Competition.resources/C8D7D470-141C-4985-B463-A7C355237157.jpg)", "- ")
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
