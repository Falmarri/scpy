'''
Created on Dec 12, 2010

@author: falmarri
'''
from setuptools import setup
setup(
    name = "scpy",
    version = "1.1.5",
    packages = ['scpy'],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['pyinotify', 'pexpect'],
    entry_points = {
        'console_scripts' : [
            'scpy = scpy:main',
            ],
        },

    # metadata for upload to PyPI
    author = "Falmarri",
    author_email = "psychicsurgeon@gmail.com",
    description = "File/Directory syncing over scp",
    long_description=open('README.rst','r').read(),
    license = "GPL",
    keywords = "scp sync autosync",
    url = "http://weaknweary.blogspot.com/2010/10/python-enhancement-to-scp.html",   # project home page, if any

    classifiers=['Topic :: System :: Networking',
                 'Intended Audience :: Developers',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Utilities',
                 ]


    # could also include long_description, download_url, classifiers, etc.
)
