#!/usr/bin/env python

import socket
import ssl
import sys
import time
import re
from optparse import OptionParser

def recv_timeout(s,timeout=2):
    s.setblocking(0)
    total_data=[];
    data='';
    begin=time.time()
    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = s.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except Exception:
            pass
    return ''.join(total_data)

def exec_cmd(s, argv):
    argv = argv.split(' ')
    print '[+] CMD = %s' % argv[0]
    print '[+] ARGS = %s' % argv[1:]

def parse_data(s, data):
    print data
    for m in re.finditer('!(cmd1[^\r\n]*)[\r\n]+', data):
        exec_cmd(s, m.group(1))

def main(server, port, channel, nick, use_ssl):
    if use_ssl:
        s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))

    # Print server info and motd
    print recv_timeout(s)

    # Set nick and connect to the channel
    s.send('NICK %s\r\n' % nick)
    s.send('USER %s %s %s %s\r\n' % (nick, nick, nick, nick))
    s.send('JOIN %s\r\n' % channel)
    s.send('PRIVMSG %s :[+] %s up and running!\r\n' % (channel, nick))

    # Wait for commands
    while True:
        data = recv_timeout(s)
        parse_data(s, data)

if __name__ == '__main__':
    parser = OptionParser(usage='%prog [options] server port channel')
    parser.add_option('-n', '--nick', dest='nick', default='pybot',
        help='bot nickname')
    parser.add_option('-S', '--ssl', action='store_true', dest='ssl',
        default=False, help='use ssl')
    (options, args) = parser.parse_args()

    if len(args) == 3:
        main(args[0], int(args[1]), args[2], options.nick, options.ssl)
    else:
        parser.print_usage()
