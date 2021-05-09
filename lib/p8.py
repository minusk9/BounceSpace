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


HELP_MESSAGE = """
P8 (Play 8)

Usage:
    [PATH]p8.py [-h] [--config=STRING] [--play=GAME]

Options:
    --config    config STRING
    --play      play GAME (default bits)
    -h          this help
"""


def _print_help():
    print(HELP_MESSAGE, file=sys.stderr)


def main(args, options):
    if "-h" in options:
        _print_help()
        sys.exit()

    if options.get("--play", "bits") == "bits":
        # FIXME the game must load the framework, not the other way around
        config = options.get("--config", "")
        game = bits.BITS(
            os.path.join(os.path.dirname(sys.argv[0]), ".."),
            play8.config_parse(config)
        )
        game.play()


# play8
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "h", ["config=", "play="])
    opts = {k: v for k, v in opts}
    main(args, opts)
