#!/usr/bin/env python

import re
import socket
import ssl
import sys

from utils import recv_timeout

class IRCBot:
    def __init__(self):
        self.server = ''
        self.port = 6697
        self.channel = '#pybot'
        self.ssl = True
        self.nick = 'pybot'
        self.password = ''
        self.socket = None

    def exec_cmd(self, argv):
        argv = argv.split(' ')
        print '[+] CMD = %s' % argv[0]
        print '[+] ARGS = %s' % argv[1:]

    def parse_data(self, data):
        print 'Received data = {\n%s\n}' % data
        for m in re.finditer('!(cmd1[^\r\n]*)[\r\n]+', data):
            self.exec_cmd(m.group(1))

    def connect(self, server, port, channel):
        self.server = server
        self.port = port
        self.channel = channel

        if self.ssl:
            self.socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((self.server, self.port))

        # Print server info and motd
        print recv_timeout(self.socket)

        # Set nick and connect to the channel
        self.socket.send('NICK %s\r\n' % self.nick)
        self.socket.send('USER %s %s %s %s\r\n' % (self.nick, self.nick, self.nick, self.nick))
        self.socket.send('JOIN %s\r\n' % self.channel)
        self.socket.send('PRIVMSG %s :[+] %s up and running!\r\n' % (self.channel, self.nick))

        # Wait for commands
        while True:
            data = recv_timeout(self.socket)
            self.parse_data(data)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def set_nick(self, nick):
        self.nick = nick

    def set_ssl(self, use_ssl):
        self.ssl = use_ssl

    def set_password(self, password):
        self.password = password
