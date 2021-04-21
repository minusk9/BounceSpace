# Play8

# Play
# Play8 9
# Written by Athos Toniolo

# use os path pygame pygame image
import os.path
import pygame
import pygame.image

# bytes shape
def bytes_shape(line, size):
	l = list()
	for x in range(0, len(line), size):
		i = x + size
		l.append(line[x:i])
	return l

# config parse
def config_parse(config):
	d = dict()
	for x in config.split(';'):
		if x:
			l = x.split(':', 1)
			if 1 < len(l):
				d[l[0]] = l[1]
			else:
				d[x] = str()
	return d

# screen64 screen
def screen64_screen(fore):
	if fore:
		return 108, 94, 181
	return 53, 40, 121

# screen64 font
def screen64_font(path, bank):
	s = "bank_{0}.p8.png"
	i = pygame.image.load(os.path.join(path, "res", s.format(bank)))
	return i.convert()

# screen64 make
def screen64_make(font, rows):
	i = len(rows[0])
	t = 16 * i, 16 * len(rows)
	s = pygame.Surface(t)
	i = 0
	for x in rows:
		t = 0, i
		screen64_printrow(font, x, s, t)
		i += 1
	return s

# screen64 view
def screen64_view(size, back=None):
	i, i2 = size
	t = 0, 0
	t2 = 16 * i, 16 * i2
	if back:
		return back.subsurface(pygame.Rect(t, t2))
	pygame.display.set_mode(t2)
	return pygame.display.get_surface()

# screen64 printall
def screen64_printall(font, rows, dest, spos):
	i, i2 = spos
	for x in rows:
		t = i, i2
		screen64_printrow(font, x, dest, t)
		i2 += 1
	return i, i2

# screen64 printrow
def screen64_printrow(font, line, dest, spos):
	i, i2 = spos
	for x in line:
		t = 16 * i, 16 * i2
		r = pygame.Rect(16 * x, 0, 16, 16)
		dest.blit(font, t, r)
		i += 1
	return i, i2

# screen64 progress
def screen64_progress(font, rvrs, progress, line, dest, spos):
	i = int(progress * len(line))
	r = screen64_printrow(rvrs, line[:i], dest, spos)
	screen64_printrow(font, line[i:], dest, r)
	return
