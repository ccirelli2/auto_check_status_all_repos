# auto_check_status_all_repos
Simple script to identify all github repositories in a given directory, check to see if they are up to date, and allow the user to commit and push changes to the master.  The script could save someone a lot of time if they had a lot of repositories in one directory and didn't know their status. 

### Usage
```
> main --help
usage: main [-h] {commit,c,auto-commit,a} ...

optional arguments:
  -h, --help            show this help message and exit

Commands:

  {commit,c,auto-commit,a}
```

```
> main commit --help
usage: main commit [-h] [-d DIR] [-m MSG] [-y]

Commit all changes, manually filling in commit messages.

optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Directory to start looking for git repos.
  -m MSG, --msg MSG  Provide a commit message.
  -y, --dry          Print commands but do not run.
```

```
> main auto-commit --help
usage: main auto-commit [-h] [-d DIR] [-m MSG] [-y]

Commit all changes using a common comit message. This will default to "quick
commit

optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Directory to start looking for git repos. Be careful of
                     shell expansion. Wrap relative paths in single quotes.
  -m MSG, --msg MSG  Provide a commit message.
  -y, --dry          Print commands but do not run.
```
