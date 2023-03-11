from .branch import BranchCommand
from .custom import CustomCommand
from .diff import DiffCommand
from .export import ExportCommand
from .import_ import ImportCommand
from .log import LogCommand
from .pull import PullCommand
from .push import PushCommand
from .remotes import RemotesCommand
from .rm import RmAllCommand
from .status import StatusCommand
from .validate import ValidateCommand

vcstool_commands = [
    BranchCommand,
    CustomCommand,
    DiffCommand,
    ExportCommand,
    ImportCommand,
    LogCommand,
    PullCommand,
    PushCommand,
    RemotesCommand,
    RmAllCommand,
    StatusCommand,
    ValidateCommand
]

__all__ = [cmd.__name__ for cmd in vcstool_commands]

_commands = [c.command for c in vcstool_commands]
if len(_commands) != len(set(_commands)):
    raise RuntimeError(
        'Multiple commands share the same command name: ' +
        ', '.join(sorted(_commands)))
