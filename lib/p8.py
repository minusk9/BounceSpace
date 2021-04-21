#!/usr/bin/python3

# Play8

# P8
# Play8 9
# Written by Athos Toniolo

# p8
def p8_0(args, opts, optv):
	if "-h" in optv:
		sys.stderr.write("P8 (Play 8)\n\nUsage:\n\t[PATH]p8.py [-h] [--config=STRING] [--play=GAME]\n\nOptions:\n\t--config\tconfig STRING\n\t--play\tplay GAME (default bits)\n\t-h\tthis help\n")
		sys.exit()
	if opt_play(opts) == 'bits':
		g = bits.BITS(os.path.join(os.path.dirname(sys.argv[0]), ".."), play8.config_parse(opt_config(opts)))
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
import bits, getopt, os.path, play8, sys
opts, args = getopt.getopt(sys.argv[1:], "h", ["config=", "play="])
p8_0(args, opts, [x for x, x2 in opts])
