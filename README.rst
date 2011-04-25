============
    scpy
============

scpy is a command line tool to autosync files and directories to remote servers over ssh. For windows users, there is a program called winscp that can automatically keep a remote directory up to date with a local one. I didn't find a tool I liked to do this on linux, so I made this one.

It follows the usage of the regular scp command with a couple of slight differences.

* There is no need to supply the -r option for directories. It determines itself whether it's a directory or not

* You can only push files to remote servers, you can't pull them back

* There is no globbing support (yet)


Usage Examples
==============
::

    scpy workspace/src username@192.168.1.2:/

This will sync the local folder ./workspace/src to /src on 192.168.1.2. It overwrites the src folder on the remote machine.::

    scpy workspace/src/file1.py workspace/src/file2.py username@192.168.1.2:workspace/src/

This will synchronize the 2 local files file1.py and file2.py to /home/username/workspace/src/ on 192.168.1.2::

    scpy workspace/src/file1.py workspace/src/file2.py username@192.168.1.2:workspace/src/ otherusername@host.com:/opt/

This is the same as above but it will sync the same files to both 192.168.1.2 and host.com