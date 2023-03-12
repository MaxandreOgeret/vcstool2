import argparse
import os
import shutil
import sys
import urllib.request as request
import re

from vcstool2.commands.import_ import file_or_url_type, get_repositories
from vcstool2.executor import ansi
from vcstool2.streams import set_streams

from .command import Command, existing_dir


class RmAllCommand(Command):
    command = "rm"
    help = "Remove the directories indicated by the list of given repositories"

    def __init__(self, *args, **kargs):
        super(RmAllCommand, self).__init__(*args, **kargs)


_cls = RmAllCommand


def get_parser():
    parser = argparse.ArgumentParser(
        description=_cls.help, prog="vcs {}".format(_cls.command))
    group = parser.add_argument_group("Command parameters")
    group.add_argument(
        "--input",
        type=file_or_url_type,
        default="-",
        help="Where to read YAML from",
        metavar="FILE_OR_URL",
    )
    group.add_argument(
        "path",
        nargs="?",
        type=existing_dir,
        default=os.curdir,
        help="Base path to look for repositories",
    )
    group.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Force the removal of the paths",
    )

    exclusive_group = parser.add_mutually_exclusive_group(required=True)

    exclusive_group.add_argument(
        "-p",
        "--pattern",
        type=str,
        help="Regex pattern used to filter paths to delete (cannot be used with -a/--all)",
    )

    exclusive_group.add_argument(
        "-a",
        "--all",
        action='store_true',
        help="Delete all (cannot be used with -p/--pattern)",
    )

    return parser


def main(args=None, stdout=None, stderr=None):
    # CLI Parsing
    set_streams(stdout=stdout, stderr=stderr)
    parser = get_parser()
    parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    args = parser.parse_args(args)
    try:
        input_ = args.input
        if isinstance(input_, request.Request):
            input_ = request.urlopen(input_)
        repos = get_repositories(input_)
    except (RuntimeError, request.URLError) as e:
        print(ansi("redf") + str(e) + ansi("reset"), file=sys.stderr)
        return 1
    args = vars(args)

    # Get the paths to the repos based on the source and the repo name
    paths = [os.path.join(args["path"], rel_path) for rel_path in repos]

    if not args["force"]:
        print(ansi("yellowf") + "Dry run (use --force to delete)." + ansi("reset"))

    err = False

    for p in paths:
        if not (args["all"] or re.search(args["pattern"], p)):
            continue

        print(p, end=': ')

        if not args["force"]:
            print(ansi("yellowf") + "skipped" + ansi("reset"))
            continue

        if not os.path.exists(p):
            print(ansi("yellowf") + "not found" + ansi("reset"))
            continue

        try:
            shutil.rmtree(p, ignore_errors=False)
        except Exception as e:
            print(ansi("redf") + "error: " + str(e) + ansi("reset"))
            err = True
            continue

        print(ansi("greenf") + "deleted" + ansi("reset"))

    if err:
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
