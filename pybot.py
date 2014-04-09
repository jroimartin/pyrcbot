#!/usr/bin/env python

import socket
import ssl
import sys
import time
import re

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

def exec_cmd(s, channel, cmd):
    cmd = cmd.split(' ')
    s.send('PRIVMSG %s :[+] CMD = %s\r\n' % (channel, cmd[0]))
    s.send('PRIVMSG %s :[+] ARGS = %s\r\n' % (channel, cmd[1:]))

def main(server, port, channel, nick='pybot'):
    #s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))

    # Print server info and motd
    print recv_timeout(s)

    # Set nick and connect to the channel
    s.send('NICK %s\r\n' % nick)
    s.send('USER %s %s %s %s\r\n' % (nick, nick, nick, nick))
    s.send('JOIN %s\r\n' % channel)
    s.send('PRIVMSG %s :[+] %s up and running!\r\n' % (channel, nick))

    # Whait for commands
    while True:
        data = recv_timeout(s)
        for m in re.finditer('!(cmd1[^\r\n]*)[\r\n]+', data):
            exec_cmd(s, channel, m.group(1))
        print data

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    elif len(sys.argv) == 5:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
    else:
        print 'usage: %s server port channel [nick]' % sys.argv[0]
        sys.exit(1)
