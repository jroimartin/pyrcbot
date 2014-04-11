#!/usr/bin/env python

import os
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
        self.plugins = []
        self.load_plugins(os.path.dirname(os.path.realpath(__file__))+'/plugins')
        self.socket = None

    def parse_data(self, data):
        print 'Received data = {\n%s\n}' % data
        for p in self.plugins:
            for m in re.finditer(p.get_regexp(), data):
                ret = p.cmd(m)
                if ret: self.socket.send('PRIVMSG %s :[+] %s\r\n' % (self.channel, ret))
        if re.search('^!help', data, re.MULTILINE):
            for p in self.plugins:
                self.socket.send('PRIVMSG %s :[+] %s\r\n' % (self.channel, p.get_help()))
        for m in re.finditer('(PING[^\r\n]*)[\r\n]+', data):
            self.socket.send('PONG %s\r\n' % m.group(1).split(' ')[1])

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
            try:
                self.parse_data(data)
            except Exception:
                self.socket.send('PRIVMSG %s :[+] Wrong syntax\r\n' % self.channel)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def load_plugins(self, path):
        if not path in sys.path:
            sys.path.append(path)
        files = filter(lambda f: f.endswith('.py'), os.listdir(path))
        modules = map(__import__, map(lambda f: os.path.splitext(f)[0], files))
        plugins = map(lambda p: getattr(p, 'IRCPlugin')(), modules)
        self.plugins.extend(plugins)
        for p in plugins:
            print "Loaded plugin:", p.__class__

    def set_nick(self, nick):
        self.nick = nick

    def set_ssl(self, use_ssl):
        self.ssl = use_ssl

    def set_password(self, password):
        self.password = password
