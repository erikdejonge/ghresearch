

def parsefile(filename, domain):
    import os
    write = False
    filename = os.path.join(os.path.expanduser("~/Desktop"), filename)


    for l in open(filename):
        if "CNAME" in l and write:
            write = False
        if write:
            if "[Remove" in l:
                pass
            else:
                if "Default" not in l and "." not in l and "(" not in l:
                    host = l.replace("\n", "")

                    print("echo 'alias ssh-"+host+"=\"ssh rabshakeh@" + host + "."+domain+"\"' >> ~/.bash_profile")
        if "AAAA" in l:
            write = True




#parsefile("chb.md", "customerheartbeat.com")
parsefile("active8.nl.md", "active8.nl")