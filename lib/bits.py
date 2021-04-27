# Play8

# BITS
# Play8 9
# Written by Athos Toniolo

import math
import os.path
import random
import sys

import configparser
import numpy
import numpy.linalg
import pygame
import pygame.display
import pygame.event
import pygame.image
import pygame.mouse
import pygame.sprite
import pygame.time

import play8


class BITS:
    """BITS"""

    def __init__(self, path, conf):
        pygame.init()
        t = 40, 25
        self.view = play8.screen64_view(t)
        pygame.display.set_caption('BITS')
        self.font = list()
        for x in range(4):
            self.font.append(play8.screen64_font(path, x))
        self.path = path
        self.ship = play8.screen64_make(
            self.font[0],
            play8.bytes_shape(bytes.fromhex("4e 4d 66 66 66 66 4d 4e"), 2)
        )
        return

    def body(self):
        cp = configparser.ConfigParser()
        cp.read(os.path.join(self.path, "ini", "bits.ini"))
        t = 35, 25
        s = play8.screen64_view(t, back=self.view)
        s2 = str()
        i = self.look(s2.join(self.code), cp)
        if pygame.mixer:
            pygame.mixer.music.load(
                os.path.join(self.path, "res", "bounce.mp3")
            )
            pygame.mixer.music.set_volume(0.3)
        while True:
            s2 = str(i)
            if not cp.has_section(s2):
                return True
            if not self.turn(s, s2, cp):
                return False
            i += 1

    def head(self):
        self.view.fill(play8.screen64_screen(False))
        t = 5, 5
        play8.screen64_printall(
            self.font[0],
            play8.bytes_shape(
                bytes.fromhex(
                    "70 43 49 42 20 42 6b 43 73 42 20 42 6d 43 4b"
                ),
                3
            ),
            self.view,
            t
        )
        t = 8, 9
        s = "OUNCE IN THE SPACE"
        play8.screen64_printrow(self.font[2], s.encode('ascii'), self.view, t)
        t = 5, 20
        s = "WRITTEN BY ATHOS TONIOLO"
        play8.screen64_printrow(self.font[2], s.encode('ascii'), self.view, t)
        t = 35, 0
        play8.screen64_printall(
            self.font[0], play8.bytes_shape(bytes.fromhex("61") * 25, 1),
            self.view,
            t
        )
        t = 36, 1
        s = "TIME"
        play8.screen64_printrow(self.font[2], s.encode('ascii'), self.view, t)
        t = 36, 5
        s = "PRESS SPACE"
        play8.screen64_printall(self.font[2], play8.bytes_shape(
            s.encode('ascii'), 1), self.view, t
        )
        b = True
        s = str()
        lst = list("CODE")
        t = 36, 23
        while True:
            if b:
                s2 = s.join(lst)
                play8.screen64_printrow(
                    self.font[2], s2.encode('ascii'), self.view, t
                )
                pygame.display.flip()
                b = False
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.KEYDOWN:
                    if x.unicode == ' ':
                        self.code = lst
                        return
                    elif len(x.unicode) == 1:
                        if x.unicode.isalpha() or x.unicode.isdigit():
                            lst.pop(0)
                            lst.append((x.unicode.upper()))
                            b = True

    def look(self, code, info):
        i = 1
        s = str(i)
        while info.has_section(s):
            if code == info.get(s, 'label'):
                return i
            i += 1
            s = str(i)
        return 1

    def play(self):
        while 1:
            self.head()
            if self.body():
                self.tail()

    def side(self, view, part, info):
        s = "{:0>4}"
        t = 36, 21
        s2 = s.format(part)
        play8.screen64_printrow(self.font[2], s2.encode('ascii'), view, t)
        t = 36, 23
        s = info.get(part, 'label')
        play8.screen64_printrow(self.font[2], s.encode('ascii'), view, t)
        i = 0
        s = "GET READY !"
        l1 = play8.bytes_shape(s.encode('ascii'), 1)
        s = "           "
        l2 = play8.bytes_shape(s.encode('ascii'), 1)
        t = 36, 5
        pygame.time.set_timer(pygame.USEREVENT, 500)
        while i < 8:
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.USEREVENT:
                    i += 1
            if i % 2:
                play8.screen64_printall(self.font[2], l1, view, t)
            else:
                play8.screen64_printall(self.font[2], l2, view, t)
            pygame.display.flip()
        pygame.time.set_timer(pygame.USEREVENT, 0)
        return

    def tail(self):
        t = play8.screen64_screen(False)
        i = 360
        s = "PRESS SPACE"
        b = True
        pygame.time.set_timer(pygame.USEREVENT, 500)
        c = pygame.time.Clock()
        while b:
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.KEYDOWN:
                    if x.unicode == ' ':
                        b = False
            self.view.fill(t)
            i2 = pygame.transform.rotate(self.ship, i)
            t2 = 100, 100
            r = self.ship.get_rect(topleft=t2)
            t2 = r.center
            r = i2.get_rect(center=t2)
            self.view.blit(i2, r.topleft)
            t2 = 5, 20
            play8.screen64_printrow(
                self.font[2], s.encode('ascii'), self.view, t2
            )
            pygame.display.flip()
            i -= 5
            i %= 360
            c.tick(50)
        pygame.time.set_timer(pygame.USEREVENT, 0)
        return

    def turn(self, view, part, info):
        self.side(view.get_parent(), part, info)
        b = True
        f = 0
        g = pygame.sprite.GroupSingle(Player(view, self.font, self.ship))
        b2 = Balls()
        for x in range(info.getint(part, 'balls')):
            b2.add(Ball(view, self.font, info.getint(part, 'speed')))
        t = play8.screen64_screen(False)
        # t2 = 0, 0
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        if pygame.mixer:
            pygame.mixer.music.play()
        c = pygame.time.Clock()
        while b:
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.USEREVENT:
                    f += 0.017
            if f >= 1:
                b = False
            self.update_progress(view.get_parent(), f)
            g.sprite.move()
            if pygame.sprite.spritecollideany(g.sprite, b2):
                if pygame.mixer:
                    s = pygame.mixer.Sound(
                        os.path.join(self.path, "res", "noise_5.1.wav")
                    )
                    s.play()
                b = False
            b2.move()
            view.fill(t)
            g.draw(view)
            b2.draw(view)
            pygame.display.flip()
            c.tick(50)
        pygame.time.set_timer(pygame.USEREVENT, 0)
        if pygame.mixer:
            pygame.mixer.music.stop()
            while pygame.mixer.get_busy():
                pass
        view.fill(t)
        pygame.display.flip()
        return f >= 1

    def update_progress(self, view, progress):
        t = 36, 1
        s = "TIME"
        play8.screen64_progress(
            self.font[2], self.font[3], progress, s.encode('ascii'), view, t
        )
        return


class Ball(pygame.sprite.Sprite):
    "Ball"

    def __init__(self, view, font, spar):
        o = super()
        o.__init__()
        self.image = play8.screen64_make(
            font[0], play8.bytes_shape(bytes.fromhex("51"), 1)
        )
        self.rect = self.image.get_rect()
        self.area = view.get_rect()
        if random.randint(0, 1):
            self.rect.left = random.randint(
                self.area.left, self.area.right - self.rect.width
            )
            self.rect.top = self.area.top
            if random.randint(0, 1):
                self.rect.top = self.area.bottom - self.rect.height
        else:
            self.rect.left = self.area.left
            if random.randint(0, 1):
                self.rect.left = self.area.right - self.rect.width
            self.rect.top = random.randint(
                self.area.top, self.area.bottom - self.rect.height
            )
        f = 2 * math.pi * random.random()
        t = spar * math.cos(f), spar * math.sin(f)
        self.move = numpy.array(t)
        self.safe = False
        return


class Balls(pygame.sprite.Group):
    "Balls"

    def move(self):
        for x in self.sprites():
            x.rect.move_ip(int(x.move[0]), int(x.move[1]))
            if x.rect.left < x.area.left and x.move[0] < 0:
                x.move[0] = - x.move[0]
            elif x.area.right < x.rect.right and 0 < x.move[0]:
                x.move[0] = - x.move[0]
            if x.rect.top < x.area.top and x.move[1] < 0:
                x.move[1] = - x.move[1]
            elif x.area.bottom < x.rect.bottom and 0 < x.move[1]:
                x.move[1] = - x.move[1]
        b = self.copy()
        for x in self.sprites():
            b.remove(x)
            l1 = pygame.sprite.spritecollide(x, b, False)
            if not l1:
                x.safe = True
            for y in l1:
                t = (
                    y.rect.centerx - x.rect.centerx,
                    y.rect.centery - x.rect.centery
                )
                a = numpy.array(t)
                f = numpy.linalg.norm(a)
                if x.safe and y.safe and f:
                    self.bounce(x, y, a, f)
                    x.safe = False
                    y.safe = False
                    b.remove(y)
        return

    def bounce(self, spra, sprb, diff, norm):
        f = norm ** 2
        a = (numpy.dot(spra.move, diff) / f) * diff
        a2 = (numpy.dot(sprb.move, diff) / f) * diff
        spra.move += a2 - a
        sprb.move += a - a2
        return


class Player(pygame.sprite.Sprite):
    "Player"

    def __init__(self, view, font, ship):
        o = super()
        o.__init__()
        self.image = ship
        self.rect = self.image.get_rect()
        self.area = view.get_rect()
        self.rect.center = self.area.width / 2, self.area.height / 2
        pygame.mouse.set_visible(0)
        pygame.mouse.set_pos(self.rect.topleft)
        return

    def move(self):
        i, i2 = pygame.mouse.get_pos()
        if (
            i >= self.area.left and self.area.right >= self.rect.width + i
            and i2 >= self.area.top
            and self.area.bottom >= self.rect.height + i2
        ):
            self.rect.left = i
            self.rect.top = i2
        return
