#!/usr/bin/env python2
'''
Created on Nov 14, 2010

@author: falmarri
'''
import sys, re
from os import path
from getpass import getpass
import  pexpect, pyinotify
from optparse import OptionParser



__author__ = "Falmarri <psychicsurgeon@gmail.com>"
__version__ = "1.1.5"


_localDirs = []
_remoteSites ={}

options = ''

credentials = {}
expected = ['The authenticity of host', 'Permission denied', 'Password', pexpect.EOF, pexpect.TIMEOUT]

_ERROR = 1
_DENIED = 2
_OK = 0

wm = pyinotify.WatchManager()

def scp( localfile, remotehost, remotepath, password=None, opts = '' ):
    """
    @param localfile: The local file to send
    @param remotehost: usernam@remotehost
    @param remotepath: The path to send the file to
    """
    passw = password or _pass_request(remotehost)

    scpcmd = "scp {0} {1} {2}:{3}".format(opts, localfile, remotehost, remotepath )
    import ipdb
    ipdb.set_trace()
    child = pexpect.spawn( scpcmd)
    index = child.expect( expected )
    if index == 0:
        child.sendline( 'yes' )
        index = child.expect( expected )

    if index == 2:
        child.sendline( passw )
        index = child.expect( expected )


    if index == 1:
        child.close()
        _pass_request(remotehost, denied=True)
        return (_DENIED, 'Permission Denied')

    else:
        child.close()
        return (_OK, '') if child.exitstatus==0 else (_ERROR, child.before)


    """
    if index == 1:
        child.sendcontrol('c')
        return _DENIED
    elif index == 3:
        print 'Connection refused...'
        return _REFUSED
    elif index == 4:
        return expected[index]
    elif index == 5:
        print 'Timed out...'
    index = child.expect( ['denied', pexpect.EOF] )
    if index == 0:
        passw = _pass_request(remotehost)
        child.sendline(passw)

    """


def mkdir( self ):
    if self.loginto not in credentials:
        raise Exception

    mkd = [self.loginto , "'mkdir " + self.local + "'"]

    mkdircmd = 'ssh ' + " ".join( mkd )

    child = pexpect.spawn( 'ssh', mkd )

    child.send( self.credentials[self.loginto] )

def _pass_request( host, check=False, denied=False):
    if denied:
        del credentials[host]
        return

    if not check and host in credentials:
        return credentials[host]

    else:
        password = getpass( "Enter password for " + host + ':' )
        credentials[host] = password
        return password

def pushRemoteSites(  pathname, dir=False ):

    which = ''

    isdir = ''

    if dir or path.isdir( pathname ):
        isdir = '-r'

    for l in _localDirs:
        if pathname.startswith( l ):
            which = path.relpath( pathname, path.dirname( l ) ) if not isdir else ''
            break

    print '\nSyncing %s...' % pathname
    for host, dest in _remoteSites.iteritems():
        print 'with %s...' % host
        for _ in range(3):
            ret, msg = scp(pathname, host, path.join(dest, which), opts=isdir)
            if ret == _DENIED:
                print msg
            elif ret == _ERROR:
                print msg
                sys.exit(1)
            else:
                print 'Done!'
                break
        else:
            sys.exit(1)

def main():
    '''Main to be used with python < 2.7'''

    description = """ """
    usage = "usage: %prog [options] local username@remote:(/)destination"
    version = "%prog v " + __version__

    parser = OptionParser( usage=usage , version=version , description = description)
#    parser.add_option( "-c", "--config", dest="config", type="string",
#                help="CONFIG file to store logins", metavar="CONFIG" )
    parser.add_option( "-s", "--no-sync", dest="sync", action="store_false",
                help="Don't sync all directories on startup", default=True )
#    parser.add_option( "-x", "--exclude", dest="exclude", type="string" )
#    parser.add_option( "-w", "--wait", dest="wait", action="store_true",
#                help="Wait for user input before syncing. Excludes initial sync", default=False)

    global options
    options, args = parser.parse_args()

    ( x.strip() for x in args )

    if len( args ) < 2:
        parser.error( "Incorrect number of arguments" )

    remotere = re.compile( r"(?P<all>(?P<host>\w+@(?:(?:(?:(?:[0-9]){1,3}.?){4})|(?:([0-9\w\.])+))):(?P<dest>.*))" )
    localre = re.compile( r"^(/?(?:(?<!@).(?!@))*)$" )


    for arg in args:
        if remotere.match( arg ):
            r = remotere.search( arg )
            _remoteSites[r.groupdict()['host']] = r.groupdict()['dest']
        elif localre.match( arg ):
            _localDirs.append( path.abspath(arg) )
        else:
            parser.error( "Incorrect argument: " + arg )

    if not _localDirs or not _remoteSites:
        parser.error( "Must include at least 1 local directory and 1 remote directory" )


    if options.sync:
        print 'Pushing local files...'
        for l in _localDirs:
            pushRemoteSites(l)
        print 'Initial sync done.'

    initWatcher()


class OnChangeHandler( pyinotify.ProcessEvent ):

    def process_IN_CREATE( self, event ):
        if not event.dir: pushRemoteSites( event.pathname )
        else:
            pass
            #_create_dir( '', self.remotes, event.pathname )

    def process_IN_MODIFY( self, event ):
        if options.wait:
            pass
        #pushRemoteSites( event.pathname )

    def process_IN_CLOSE_WRITE(self, event):
        pushRemoteSites( event.pathname )

    def process_IN_DELETE( self, event ):
        #if self.options.delete: _delete(self, locals[0], self.remotes)
        pass


def initWatcher():


    # Watch Manager
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE# watched events

    notifier = pyinotify.Notifier( wm, OnChangeHandler( ) )

    for x in _localDirs:
        wm.add_watch( x, mask, rec=True, auto_add=True )


    notifier.loop()


if __name__ == '__main__':
    main()
