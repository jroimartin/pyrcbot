#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

from pyrcbot.ircbot import IRCBot

parser = OptionParser(usage='%prog [options] server port channel')
parser.add_option('-n', '--nick', dest='nick', default='pybot',
    help='set bot nickname')
parser.add_option('-s', '--ssl', action='store_true', dest='ssl',
    default=False, help='use ssl')
parser.add_option('-p', '--password', dest='password', default='',
    help='set IRC password to connect')
(options, args) = parser.parse_args()

if len(args) == 3:
    bot = IRCBot()
    bot.set_nick(options.nick)
    bot.set_ssl(options.ssl)
    bot.set_password(options.password)
    try:
        bot.connect(args[0], int(args[1]), args[2])
    except Exception as e:
        print 'Error:', e
        sys.exit(1)
    except KeyboardInterrupt:
        print 'Disconnecting bot...' 
    finally:
        bot.close()
else:
    parser.print_usage()
