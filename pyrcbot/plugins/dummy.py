#!/usr/bin/env python

# Copyright 2014 The pyrcbot Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

class IRCPlugin:
    def get_help(self):
        return '!dummy - dummy command'

    def get_regexp(self):
        return ':(!dummy[^\r\n]*)'

    def cmd(self, match, auth = None):
        argv = match.group(1).split(' ')
        ret = 'CMD = %s ; ARGS = %s\r\n' % (argv[0], argv[1:])
        return ret
