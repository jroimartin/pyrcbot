#!/usr/bin/env python

class IRCPlugin:
    def get_help(self):
        print '!dummy - dummy command'

    def get_regexp(self):
        print '!dummy'

    def cmd(self, *args):
        print 'CMD = cmd'
        print 'ARGS =', args
