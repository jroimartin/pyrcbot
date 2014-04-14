#!/usr/bin/env python

# Copyright 2014 The pyrcbot Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

class IRCPlugin:
    def get_help(self):
        return '!dummy - dummy command'

    def get_regexp(self):
        return r':(.+?)!.+? PRIVMSG (.+?) :(!dummy[^\r\n]*)'

    def cmd(self, match, ircbot):
        if match.group(2) == ircbot.nick:
            dst = match.group(1)
        else:
            dst = ircbot.channel

        argv = match.group(3).split(' ')
        ircbot.privmsg(dst, '[+] CMD = %s ; ARGS = %s' % (argv[0], argv[1:]))

    def close(self):
        print '[%s] closing...' % self.__class__
