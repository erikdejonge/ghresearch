#!/usr/bin/env python3
# coding=utf-8
"""
Search github repositories

Usage:
  githubsearch.py [options] [--] <username> <password> <target_dir> <numdays> <min_stars> <keyword>

Options:
  -h --help     Show this screen.
  -c --clone    Clone the repositories found

Description:
    username   :  Github username
    passwprd   :  Github passwprd
    target_dir :  Folder to check and store results
    min_stars  :  Minimum number of stars
    numdays    :  Must be commit activity in last num days

Active8 (18-05-15)
author: erik@a8.nl
license: GNU-GPL2
"""
import os
import pytz

from git import Repo

import time
import datetime
import arguments

from consoleprinter import console
from dateutil.parser import parse
from github import Github, GithubException
from cmdssh import call_command


class IArgument(arguments.Arguments):
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
        self.clone = False
        self.help = False
        self.keyword = ""
        self.min_stars = 0
        self.numdays = 0
        self.password = ""
        self.target_dir = ""
        self.username = ""
        super().__init__(doc, validateschema, argvalue, yamlstr, yamlfile, parse_arguments, persistoption, alwaysfullhelp, version, parent)


def main():
    """
    main
    """
    arg = IArgument(__doc__)
    keyword = arg.keyword
    targetdir = os.path.join(os.path.expanduser(arg.target_dir), arg.keyword.replace(" ", "_").replace("/", ""))
    min_stars = arg.min_stars
    clone = arg.clone
    g = Github(arg.username, arg.password)
    results = []
    cnt = 0

    for p in g.search_repositories(keyword, "stars"):
        results.append(p)

        if len(results) % 100 == 0:
            time.sleep(1)

        rpath = os.path.join(targetdir, p.name)

        if os.path.exists(rpath):
            console(p.stargazers_count, p.name, "skipped", color="blue")
        else:
            try:
                if clone:
                    if not os.path.exists(targetdir):
                        call_command("mkdir " + targetdir)

                    os.chdir(os.path.expanduser(targetdir))

                commitobj = p.get_branch("master").commit
                commitobj.update()
                updated_at = commitobj.last_modified
                updated = parse(str(updated_at))
                now = pytz.utc.localize(datetime.datetime.now())
            except GithubException as e:
                console(e.data["message"], color="red")

                if "API rate limit exceeded" in str(e):
                    time.sleep(120)

                now = datetime.datetime.now()
                updated_at = p.updated_at
                updated = parse(str(updated_at))

            td = now - updated
            updated = td.total_seconds() / 60 / 60

            # noinspection PyUnresolvedReferences
            if updated < arg.numdays * 24:
                # console(p)

                if p.stargazers_count < min_stars:
                    break
                else:
                    cnt += 1

                    if clone:
                        output = p.name + " " + str(Repo.clone_from(p.clone_url, p.name).active_branch) + " cloned"
                        console(cnt, p.stargazers_count, output, str(updated_at), color="green")

                #    console("skipp", str(p.name), color="blue")
            else:
                if os.path.exists(rpath):
                    print("del", rpath)

                    if clone:
                        call_command("rm -Rf " + rpath)

        # print(g.get_user().add_to_starred(p))

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


    #for r, ds, f in os.walk(arg.target_dir):

if __name__ == "__main__":
    main()
