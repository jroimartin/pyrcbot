#!/usr/bin/env python

class IRCPlugin:
    def get_help(self):
        return '!dummy - dummy command'

    def get_regexp(self):
        return '(!dummy [^\r\n]*)[\r\n]+'

    def cmd(self, match, auth = None):
        argv = match.group(1).split(' ')
        ret = 'CMD = %s\r\nARGS = %s\r\n' % (argv[0], argv[1:])
        return ret
