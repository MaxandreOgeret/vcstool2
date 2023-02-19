from .git import GitClient

vcstool_clients = [GitClient]

_client_types = [c.type for c in vcstool_clients]
if len(_client_types) != len(set(_client_types)):
    raise RuntimeError(
        'Multiple vcs clients share the same type: ' +
        ', '.join(sorted(_client_types)))
