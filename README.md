# ghresearch
Research tool for Github, downloads repositories and generates markdown and html listings

## search github

```
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
```

### alias

```bash
# github password stored in users root folder [.ghpwd]

function _searchgh() {
    python3 ~/workspace/ghresearch/githubsearch.py -c erik@a8.nl `cat ~/.ghpwd` ~/Desktop/ghresearch 1 21 "`echo "$@"`"
}

alias searchgh="_searchgh"
```

### usage

``` bash
searchgh python prompt toolkit 
<arguments.Arguments object at 0x10d5a25c0>
---
options:
  clone:  true
  help:  false

positional:
  keyword:  python prompt toolkit
  min_stars:  1
  numdays:  21
  password:  xxxxxx
  target_dir:  /Users/rabshakeh/Desktop
  username:  erik@a8.nl


1.56 | githubsearch.py:105 | 1 | 1421 | python-prompt-toolkit | Wed, 13 May 2015 17:56:01 GMT
Cloning into 'python-prompt-toolkit'...
remote: Counting objects: 3304, done.
remote: Total 3304 (delta 0), reused 0 (delta 0), pack-reused 3304
Receiving objects: 100% (3304/3304), 1.45 MiB | 1.51 MiB/s, done.
Resolving deltas: 100% (2397/2397), done.
Checking connectivity... done.
```

## convert to html

add to .bash_profile
``` bash
function _md2html() {
    echo -e "\033[0;94m"$1"\033[0;96m    ->    "$(dirname $1)"/"$(basename $1 ".md").html"\033[0m"
    pandoc --from=markdown_github --to=html --highlight-style=pygments "$(dirname $1)"/"$(basename $1)" -o "$(dirname $1)"/"$(basename $1 ".md").html.tmp"
    cat ~/workspace/ghresearch/mdhtml1.html > "$(dirname $1)"/"$(basename $1 ".md").html"
    cat ~/workspace/ghresearch/md2html.css >> "$(dirname $1)"/"$(basename $1 ".md").html"
    cat "$(dirname $1)"/"$(basename $1 ".md").html.tmp" >> "$(dirname $1)"/"$(basename $1 ".md").html"
    title=`echo $(basename $1 ".md") |  tr -d "'" | tr -d "\n" | sed -e "s/-/ /g" -e "s/_/ /g"`
    echo "<title>""${title^}""</title>" >> "$(dirname $1)"/"$(basename $1 ".md").html"
    cat ~/workspace/ghresearch/mdhtml2.html >> "$(dirname $1)"/"$(basename $1 ".md").html"
    rm "$(dirname $1)"/"$(basename $1 ".md").html.tmp"
}
function _allmd2html() {
    echo -e "\033[0;31mALL MD2HTML: "`pwd`"\033[0m"
    read -p "are you sure    (y/n)? " yn
    case $yn in
        [Nn]* ) return;;
        * ) echo "Please answer y or n.";;
    esac
    echo -e "\033[0;91mconvert all md to html recursively: "`pwd`"\033[0m"
    for mdfile in $(find . -type f -name '*md')
        do
            if [ -f $mdfile ]; then
                _md2html "$mdfile"

            fi
        done
    open "index.html"
}
alias allmd2html='_allmd2html'
```
Run conversion script, go to dir and convert md to html

```bash
python3 genindex.py ~/Desktop/ghresearch
cd ~/Desktop/ghresearch
allmd2html
```