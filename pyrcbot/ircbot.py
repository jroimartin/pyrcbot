#!/usr/bin/env python

# Copyright 2014 The pyrcbot Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

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

        # Join channel after MOTD
        if re.search(r'^.+? (?!PRIVMSG).+? .+? :End of /MOTD command', data, re.MULTILINE):
            self.send('JOIN %s' % self.channel)
            self.privmsg(self.channel, '[+] %s up and running!' % self.nick)

        # Keep alive the connection
        m = re.search(r'^PING (.+)', data, re.MULTILINE)
        if m: self.send('PONG %s' % m.group(1))

        # Call matching plugins
        for p in self.plugins:
            for m in re.finditer(p.get_regexp(), data):
                p.cmd(m, self)

    def connect(self, server, port, channel):
        self.server = server
        self.port = port
        self.channel = channel

        if self.ssl:
            self.socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((self.server, self.port))

        # Send user's info
        if self.password:
            self.send('PASS %s' % self.password)
        self.send('NICK %s' % self.nick)
        self.send('USER %s %s %s %s' % (self.nick, self.nick, self.nick, self.nick))

        # Wait for commands
        while True:
            self.send('PING %s' % self.server)
            data = recv_timeout(self.socket)
            try:
                self.parse_data(data)
            except Exception:
                pass

    def close(self):
        # Send close message to all plugins
        for p in self.plugins:
            p.close()
        self.send('QUIT :Bye!')
        self.socket.close()
        self.socket = None

    def send(self, cmd):
        self.socket.send(cmd + '\r\n')

    def privmsg(self, dst, msg):
        self.send('PRIVMSG %s :%s' % (dst, msg))

    def load_plugins(self, path):
        if path not in sys.path:
            sys.path.append(path)

        # Import non-dupped plugins
        files = filter(lambda f: f.endswith('.py'), os.listdir(path))
        modules = map(__import__, filter(lambda m: m not in sys.modules,
            map(lambda f: os.path.splitext(f)[0], files)))
        plugins = map(lambda p: getattr(p, 'IRCPlugin')(), modules)
        self.plugins.extend(plugins)

        for p in plugins:
            print "[%s] loading..." % p.__class__

    def set_nick(self, nick):
        self.nick = nick

    def set_ssl(self, use_ssl):
        self.ssl = use_ssl

    def set_password(self, password):
        self.password = password
