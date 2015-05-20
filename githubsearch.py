#!/usr/bin/env python3
# coding=utf-8
"""
Search github repositories

Usage:
  githubsearch.py [options] [--] <username> <password> <target_dir> <min_stars> <numdays> <keyword>

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
import stat
import time
import datetime
import arguments

from consoleprinter import console
from dateutil.parser import parse
from github import Github, GithubException


def main():
    """
    main
    """
    arg = arguments.Arguments(__doc__)
    print(arg)

    # noinspection PyUnresolvedReferences
    keyword = arg.keyword

    # noinspection PyUnresolvedReferences
    targetdir = os.path.expanduser(arg.target_dir)

    # noinspection PyUnresolvedReferences
    min_stars = arg.min_stars

    # noinspection PyUnresolvedReferences
    clone = arg.clone

    if clone:
        if not os.path.exists(targetdir):
            os.system("mkdir " + targetdir)

    # noinspection PyUnresolvedReferences
    g = Github(arg.username, arg.password)

    if clone:
        os.chdir(os.path.expanduser(targetdir))

    results = []
    cnt = 0

    for p in g.search_repositories(keyword, "stars"):
        results.append(p)

        if len(results) % 100 == 0:
            time.sleep(1)

        rpath = os.path.join(targetdir, p.name)

        if os.path.exists(rpath):
            console(p.name, "skipped", color="blue")
        else:
            try:
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
                    console(p.name, p.stargazers_count, color="grey")
                else:
                    cnt += 1
                    console(cnt, p.stargazers_count, p.name, str(updated_at), color="green")

                    if clone:
                        if (p.size / 100) > 5:
                            os.system("git clone " + p.clone_url + " &")
                        else:
                            os.system("git clone " + p.clone_url)

                #    console("skipp", str(p.name), color="blue")
            else:
                if os.path.exists(rpath):
                    print("del", rpath)

                    if clone:
                        os.system("rm -Rf " + rpath)

        # print(g.get_user().add_to_starred(p))

    os.system("wait")


if __name__ == "__main__":
    main()
