#!/usr/bin/python3

import getopt
import os
import sys

import bits
import play8

# Play8

# P8
# Play8 9
# Written by Athos Toniolo


# p8
def p8_0(args, opts, optv):
    if "-h" in optv:
        sys.stderr.write("""
P8 (Play 8)

Usage:
    [PATH]p8.py [-h] [--config=STRING] [--play=GAME]

Options:
    --config    config STRING
    --play      play GAME (default bits)
    -h          this help
""")
        sys.exit()
    if opt_play(opts) == 'bits':
        g = bits.BITS(
            os.path.join(os.path.dirname(sys.argv[0]), ".."),
            play8.config_parse(opt_config(opts))
        )
        g.play()
    return


# config
def opt_config(opts):
    for x, x2 in opts:
        if x == "--config":
            return x2
    return str()


# play
def opt_play(opts):
    for x, x2 in opts:
        if x == "--play":
            return x2
    return 'bits'


# play8
opts, args = getopt.getopt(sys.argv[1:], "h", ["config=", "play="])
p8_0(args, opts, [x for x, x2 in opts])
