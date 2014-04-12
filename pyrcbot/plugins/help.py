#!/usr/bin/env python

# Copyright 2014 The pyrcbot Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

class IRCPlugin:
    def get_help(self):
        return '!help - list plugins'

    def get_regexp(self):
        return r':(.+?)!.+? PRIVMSG (.+?) :!help'

    def cmd(self, match, ircbot):
        if match.group(2) == ircbot.nick:
            dst = match.group(1)
        else:
            dst = ircbot.channel

        for p in ircbot.plugins:
            ircbot.privmsg(dst, '[+] %s' % p.get_help())
