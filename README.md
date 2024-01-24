# What is vcstool2?

**ℹ️ This project is a fork of [vcstool](https://github.com/dirk-thomas/vcstool) originally created by Dirk Thomas. All credits for the original work go to Dirk Thomas. ℹ️**

Vcstool2 is a version control system (VCS) tool, designed to make working
with multiple repositories easier.

Note:

This tool should not be confused with [vcstools](https://github.com/vcstools/vcstools/) (with a trailing`s`) which
provides a Python API for interacting with different version control systems. The biggest differences between the two
are:

- **vcstool2** doesn't use any state beside the repository working copies available in the filesystem.
- The file format of vcstool2's `export` uses the relative paths of the repositories as keys in YAML which avoids
  collisions by design.
- **vcstool2** has significantly fewer lines of code than **vcstools** including the command line tools built on top.

## Python support

This package supports Python >= 3.5, and is tested on Python (3.7 -> 3.12).

## How does it work?

Vcstool2 operates on any folder from where it recursively searches for supported repositories. On these repositories
vcstool2 invokes the native VCS client with the requested command (i.e. *diff*).

## Which VCS types are supported?

Vcstool2 supports [Git](http://git-scm.com) repositories only.

## How to use vcstool2?

The script `vcs` can be used similarly to the VCS clients `git`, `hg`, etc. The `help` command provides a list of
available commands with an additional description:

```bash
vcs help
```

By default, vcstool2 searches for repositories under the current folder. Optionally one path (or multiple paths) can be
passed to search for repositories at different locations:

```bash
vcs status /path/to/several/repos /path/to/other/repos /path/to/single/repo
```

## Exporting and importing sets of repositories

Vcstool2 can export and import all the information required to reproduce the versions of a set of repositories. Vcstool2
uses a simple [YAML](http://www.yaml.org/) format to encode this information. This format includes a root
key `repositories` under which each local repository is described by a dictionary keyed by its relative path. Each of
these dictionaries contains keys `url`, and `version`. If the `version` key is omitted the default branch is
being used.

This results in something similar to the following for a set of two repositories
([vcstool](https://github.com/dirk-thomas/vcstool) and
[vcstool2](https://github.com/MaxandreOgeret/vcstool2)):

``` yaml
repositories:
  vcstool:
    url: git@github.com:dirk-thomas/vcstool.git
    version: master
  old_tools/rosinstall:
    url: git@github.com:MaxandreOgeret/vcstool2.git
    version: master
```

### Export set of repositories

The `vcs export` command outputs the path, URL and version
information for all repositories in [YAML](http://www.yaml.org/) format.
The output is usually piped to a file:

```bash
vcs export > my.repos
```

If the repository is currently on the tip of a branch the branch is followed. This implies that a later import might
fetch a newer revision if the branch has evolved in the meantime. Furthermore, if the local branch has evolved from the
remote repository an import might not result in the exact same state.

To make sure to store the exact revision in the exported data use the command line argument `--exact`. Since a specific
revision is not tied to neither a branch nor a remote (for Git and Mercurial) the tool will check if the current hash
exists in any of the remotes. If it exists in multiple the remotes `origin` and `upstream` are considered before any
other in alphabetical order.

### Import set of repositories

The `vcs import` command clones all repositories which are passed in via `stdin` in YAML format. Usually the data of a
previously exported file is piped in:

```bash
vcs import < my.repos
```

Beside passing a file path the command also supports passing a URL.

### Validate repositories file

The `vcs validate` command takes a YAML file which is passed in via `stdin` and validates its contents and format. The
data of a previously-exported file or hand-generated file are piped in:

```bash
vcs validate < my.repos
```

### Deleting repositories

The `vcs rm` command takes a YAML file containing the repositories which is passed in via `stdin` or with its path
specified via `--input`.

The command performs a dry run by default, to perform the deletion use the `--force` option.

This command will delete all the pulled repositories if the `--all` option is passed.  
It can also filter the repos to delete based on their cloning path with a regex pattern passed with the `--pattern` 
option, see the `re` module [documentation](https://docs.python.org/3/library/re.html#regular-expression-syntax) 
for details about the syntax.

To delete all:

```bash
vcs rm --all --force < repos.yaml
```

To delete all repos paths containing "foo" or "bar":

```bash
vcs rm --pattern "foo|bar" --force < repos.yaml
```

### Version ranges

Vcstool2 supports version ranges in the yaml repository file, E.g.

```yaml
repositories:
  vcstool2_0:
    url: https://github.com/MaxandreOgeret/vcstool2.git
    version: ">0.4.1,<0.4.3"
  vcstool2_1:
    url: https://github.com/MaxandreOgeret/vcstool2.git
    version: "==0.4.*"
```

The version ranges syntax follows [Python Packaging Authority Guidelines](https://peps.python.org/pep-0440/#version-specifiers), and is powered by the
[packaging](https://packaging.pypa.io/en/stable/specifiers.html) package.

## Advanced features

### Show log since last tag

The `vcs log` command supports the argument `--limit-untagged` which will output the log for all commits since the last
tag.

### Parallelization and stdin

By default `vcs` parallelizes the work across multiple repositories based on the number of CPU cores. In the case that
the invoked commands require input from `stdin` that parallelization is a problem. In order to be able to provide input
to each command separately these commands must run sequentially. When needing to e.g. interactively provide credentials
all commands should be executed sequentially by passing:

```
--workers 1
```

In the case repositories are using SSH `git@` URLs but the host is not known yet `vcs import` automatically falls back
to a single worker.

### Run arbitrary commands

The `vcs custom` command enables to pass arbitrary user-specified arguments to the git executable.

```
vcs custom --args log --oneline -n 10
```


# How to install vcstool2?

Use the [PyPI](http://pypi.python.org) package:

```bash
sudo pip install vcstool2
```

## Setup auto-completion

For the shells *bash*, *tcsh* and *zsh* vcstool2 can provide auto-completion of the various VCS commands. In order to
enable that feature the shell specific completion file must be sourced.

For *bash* append the following line to the `~/.bashrc` file:

```bash
source /usr/share/vcstool2-completion/vcs.bash
```

For *tcsh* append the following line to the `~/.cshrc` file:

```bash
source /usr/share/vcstool2-completion/vcs.tcsh
```

For *zsh* append the following line to the `~/.zshrc` file:

```bash
source /usr/share/vcstool2-completion/vcs.zsh
```

For *fish* append the following line to the `~/.config/fishconfig.fish` file:

```bash
source /usr/share/vcstool2-completion/vcs.fish
```

# How to contribute?

## How to report problems?

Before reporting a problem please make sure to use the latest version. Issues can be filled
on [GitHub](https://github.com/MaxandreOgeret/vcstool2/issues) after making sure that this problem has not yet been
reported.

Please make sure to include as much information, i.e. version numbers from vcstool2, operating system, Python and a
reproducible example of the commands which expose the problem.

## How to try the latest changes?

Sourcing the `setup.sh` file prepends the `src` folder to the`PYTHONPATH` and the `scripts` folder to the `PATH`. Then
vcstool2 can be used with the commands `vcs-COMMAND` (note the hyphen between `vcs` and`command` instead of a space).

Alternatively the `-e/--editable` flag of `pip` can be used:

```bash
# from the top level of this repo
pip3 install --user -e .
```
