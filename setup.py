from pathlib import Path
from setuptools import find_packages
from setuptools import setup

from vcstool2 import __version__

install_requires = ['PyYAML', 'setuptools', 'packaging']
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='vcstool2',
    version=__version__,
    install_requires=install_requires,
    packages=find_packages(),
    author='Dirk Thomas',
    author_email='web@dirk-thomas.net',
    maintainer='Maxandre Ogeret',
    maintainer_email='MaxandreOgeret@users.noreply.github.com',
    url='https://github.com/MaxandreOgeret/vcstool2',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Version Control',
                 'Topic :: Utilities'],
    description='vcstool2 provides a command line tool to invoke git commands on multiple repositories.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License, Version 2.0',
    data_files=[
        ('share/vcstool2-completion', [
            'vcstool2-completion/vcs.bash',
            'vcstool2-completion/vcs.tcsh',
            'vcstool2-completion/vcs.zsh',
            'vcstool2-completion/vcs.fish'
        ])
    ],
    entry_points={
        'console_scripts': [
            'vcs = vcstool2.commands.vcs:main',
            'vcs-branch = vcstool2.commands.branch:main',
            'vcs-custom = vcstool2.commands.custom:main',
            'vcs-diff = vcstool2.commands.diff:main',
            'vcs-export = vcstool2.commands.export:main',
            'vcs-git = vcstool2.commands.custom:git_main',
            'vcs-help = vcstool2.commands.help:main',
            'vcs-import = vcstool2.commands.import_:main',
            'vcs-log = vcstool2.commands.log:main',
            'vcs-pull = vcstool2.commands.pull:main',
            'vcs-push = vcstool2.commands.push:main',
            'vcs-remotes = vcstool2.commands.remotes:main',
            'vcs-rm = vcstool2.commands.rm:main',
            'vcs-status = vcstool2.commands.status:main',
            'vcs-validate = vcstool2.commands.validate:main',
        ]
    }
)
