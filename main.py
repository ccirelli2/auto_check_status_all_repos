#!/usr/bin/env python3
# Import Pyton Libraries ---------------------------------------------------
from os import path, getenv, listdir
import subprocess
import logging
import argparse

SCRIPT_NAME = path.basename(__file__)

log_level = getattr(logging, getenv('LOGLEVEL', 'NOTSET').upper(), logging.WARNING)
log_level = log_level if log_level else logging.WARNING
logging.basicConfig(level=log_level)

COMMIT_MSG = 'quick commit'
ALL_CLEAR_MSG = 'nothing to commit, working tree clean'


def NOOP(**_):
    pass


def commit_changes(start_directory, commit_msg=None):
    git_commands = []
    logging.debug("Start dir '%s'. Msg '%s'.", start_directory, commit_msg)
    for directory in [d for d in listdir(start_directory) if path.isdir(path.join(start_directory, d, '.git'))]:
        logging.debug("Found a git dir '%s'", directory)
        git_dir = path.join(start_directory, directory, '.git')
        base_cmd = ['git', '--git-dir', git_dir]

        cmd = []
        cmd.extend(base_cmd)
        cmd.append('status')
        git_status = subprocess.check_output(cmd)

        if ALL_CLEAR_MSG not in str(git_status):
            if not commit_msg:
                cmd_commit_msg = input(f"Please enter a commit message for '{directory}': ")
                cmd_commit_msg = cmd_commit_msg if cmd_commit_msg else COMMIT_MSG
            else:
                cmd_commit_msg = commit_msg

            cmd = []
            cmd.extend(base_cmd)
            cmd.extend(['add', '--all'])
            git_commands.append(cmd)

            cmd = []
            cmd.extend(base_cmd)
            cmd.extend(['commit', '-m', cmd_commit_msg])
            git_commands.append(cmd)

    return git_commands


def command_handler(args):
    git_commands = commit_changes(getattr(args, 'dir', '.'), getattr(args, 'msg', None))

    for cmd in git_commands:
        if args.dry:
            print(' '.join(cmd))
            print('No commands have been executed during this process.')
        else:
            subprocess.check_output(cmd)


def is_valid_dir(directory):
    if path.isdir(directory):
        return directory
    raise argparse.ArgumentTypeError('Not a valid directory.')


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=NOOP)
    subparsers = parser.add_subparsers(
        title='Commands',
        description='',
        help=''
    )

    parser_manual_commit = subparsers.add_parser('commit', aliases=['c'], description='Commit all changes, manually filling in commit messages.')
    parser_manual_commit.add_argument('-d', '--dir', type=is_valid_dir, default='.', help='Directory to start looking for git repos.')
    parser_manual_commit.add_argument('-m', '--msg', default=None, help='Provide a commit message.')
    parser_manual_commit.add_argument('-y', '--dry', action='store_true', help='Print commands but do not run.')
    parser_manual_commit.set_defaults(func=command_handler)

    parser_auto_commit = subparsers.add_parser('auto-commit', aliases=['a'], description=f'Commit all changes using a common comit message. This will default to "{COMMIT_MSG}')
    parser_auto_commit.add_argument('-d', '--dir', type=is_valid_dir, default='.', help='Directory to start looking for git repos. Be careful of shell expansion. Wrap relative paths in single quotes.')
    parser_auto_commit.add_argument('-m', '--msg', default=COMMIT_MSG, help='Provide a commit message.')
    parser_auto_commit.add_argument('-y', '--dry', action='store_true', help='Print commands but do not run.')
    parser_auto_commit.set_defaults(func=command_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
