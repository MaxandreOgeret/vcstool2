from .git import GitClient

vcstool_clients = [GitClient]
_client_types = [c.type for c in vcstool_clients]
