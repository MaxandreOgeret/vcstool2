import argparse
import sys

from vcstool2.crawler import find_repositories
from vcstool2.executor import execute_jobs
from vcstool2.executor import generate_jobs
from vcstool2.executor import output_repositories
from vcstool2.executor import output_results
from vcstool2.streams import set_streams

from .command import add_common_arguments
from .command import Command


class CustomCommand(Command):

    command = 'custom'
    help = 'Run a custom command'

    def __init__(self, args):
        super(CustomCommand, self).__init__(args)
        self.args = args.args


def get_parser():
    parser = argparse.ArgumentParser(
        description='Run a custom command', prog='vcs custom')
    group = parser.add_argument_group('"custom" command parameters')
    group.add_argument(
        '--args', required=True, nargs='*', help='Arbitrary arguments passed '
        'to each vcs invocation. It must be passed after other arguments '
        'since it collects all following options.')
    return parser


def main(args=None, stdout=None, stderr=None):
    set_streams(stdout=stdout, stderr=stderr)

    parser = get_parser()
    add_common_arguments(parser)

    # separate anything followed after --args to not confuse argparse
    if args is None:
        args = sys.argv[1:]
    try:
        index = args.index('--args') + 1
    except ValueError:
        # should generate error due to missing --args
        parser.parse_known_args(args)

    client_args = args[index:]
    args = parser.parse_args(args[0:index])
    args.args = client_args

    command = CustomCommand(args)

    # filter repositories by specified client types
    clients = find_repositories(command.paths, nested=command.nested)

    if command.output_repos:
        output_repositories(clients)
    jobs = generate_jobs(clients, command)
    results = execute_jobs(
        jobs, show_progress=True, number_of_workers=args.workers,
        debug_jobs=args.debug)

    output_results(results, hide_empty=args.hide_empty)

    any_error = any(r['returncode'] for r in results)
    return 1 if any_error else 0


def git_main(args=None):
    if args is None:
        args = sys.argv[1:]
    return main(['--git', '--args'] + args)


if __name__ == '__main__':
    sys.exit(main())
