#!/usr/bin/env python

# Copyright 2014 The pyrcbot Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import sys
from optparse import OptionParser

from pyrcbot.ircbot import IRCBot

parser = OptionParser(usage='%prog [options] server port channel')
parser.add_option('-n', '--nick', dest='nick', default='pybot',
    help='set bot nickname')
parser.add_option('-s', '--ssl', action='store_true', dest='ssl',
    default=False, help='use ssl')
parser.add_option('-P', '--password', dest='password', default='',
    help='set IRC password to connect')
parser.add_option('-p', '--plugins-folder', dest='plugins_folder', default='',
    help='set plugins folder')
(options, args) = parser.parse_args()

if len(args) != 3:
    parser.print_usage()
    sys.exit(1)

bot = IRCBot()
bot.set_nick(options.nick)
bot.set_ssl(options.ssl)
bot.set_password(options.password)

if options.plugins_folder:
    try:
        bot.load_plugins(options.plugins_folder)
    except Exception as e:
        print 'Error:', e
        sys.exit(1)

try:
    bot.connect(args[0], int(args[1]), args[2])
except Exception as e:
    print 'Error:', e
    sys.exit(1)
except KeyboardInterrupt:
    print 'Disconnecting bot...'
bot.close()
