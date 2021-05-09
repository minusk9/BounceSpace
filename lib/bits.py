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

    def __init__(self, path, _):
        self._caption = "BITS"
        self.path = path
        self.resolution = 40, 25
        self.ship = None
        self.view = None
        self.code = None    # XXX what is this?

        self.start()

    def start(self):
        pygame.init()   # FIXME this should be called on framework start

        self.view = play8.screen64_view(self.resolution)
        pygame.display.set_caption(self._caption)
        self.font = [play8.screen64_font(self.path, x) for x in range(4)]
        self.ship = play8.screen64_make(
            self.font[0],
            play8.bytes_shape(bytes.fromhex("4e 4d 66 66 66 66 4d 4e"), 2)
        )

    def body(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(self.path, "ini", "bits.ini"))
        playable_area_size = 35, 25
        playable_area = play8.screen64_view(playable_area_size, back=self.view)
        i = self.look("".join(self.code), config)
        if pygame.mixer:
            pygame.mixer.music.load(
                os.path.join(self.path, "res", "bounce.mp3")
            )
            pygame.mixer.music.set_volume(0.3)
        while True:
            s2 = str(i)
            if not config.has_section(s2):
                return True
            if not self.turn(playable_area, s2, config):
                return False
            i += 1

    def _write_capital_b_at(self, coords):
        play8.screen64_printall(
            self.font[0],
            play8.bytes_shape(
                bytes.fromhex(
                    "70 43 49 42 20 42 6b 43 73 42 20 42 6d 43 4b"
                ),
                3
            ),
            self.view,
            coords,
        )

    def _write_ascii_at(self, text, coords):
        play8.screen64_printrow(
            self.font[2],
            text.encode('ascii'),
            self.view,
            coords,
        )

    def head(self):
        self.view.fill(play8.screen64_screen(fore=False))
        self._write_capital_b_at((5, 5))
        self._write_ascii_at("OUNCE IN THE SPACE", (8, 9))
        self._write_ascii_at("WRITTEN BY ATHOS TONIOLO", (5, 20))

        # UI
        coords = 35, 0
        play8.screen64_printall(
            self.font[0], play8.bytes_shape(bytes.fromhex("61") * 25, 1),
            self.view,
            coords
        )
        self._write_ascii_at("TIME", (36, 1))
        coords = 36, 5
        s = "PRESS SPACE"
        play8.screen64_printall(
            self.font[2],
            play8.bytes_shape(s.encode('ascii'), 1),
            self.view,
            coords,
        )

        b = True
        s = ""
        chars = list("CODE")
        coords = 36, 23
        while True:
            if b:
                s2 = s.join(chars)
                self._write_ascii_at(s2, coords)
                pygame.display.flip()
                b = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == ' ':
                        self.code = chars
                        return
                    elif len(event.unicode) == 1:
                        if event.unicode.isalpha() or event.unicode.isdigit():
                            chars.pop(0)
                            chars.append(event.unicode.upper())
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
        while True:
            self.head()
            if self.body():
                self.tail()

    def side(self, view, part, info):
        # update sidebar
        coords = 36, 21
        self._write_ascii_at(f"{part:0>4}", coords)
        coords = 36, 23
        self._write_ascii_at(info.get(part, 'label'), coords)

        # flash a "Get ready" message
        prompt_text = "GET READY !"
        prompt_on = play8.bytes_shape(prompt_text.encode('ascii'), 1)
        prompt_off = play8.bytes_shape(
            (" " * len(prompt_text)).encode('ascii'),
            1
        )
        pygame.time.set_timer(pygame.USEREVENT, 500)
        coords = 36, 5
        i = 0
        while i < 8:    # XXX WTF??
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.USEREVENT:
                    i += 1
            if i % 2:
                play8.screen64_printall(self.font[2], prompt_on, view, coords)
            else:
                play8.screen64_printall(self.font[2], prompt_off, view, coords)
            pygame.display.flip()
        pygame.time.set_timer(pygame.USEREVENT, 0)

    def tail(self):
        bg_rgb = play8.screen64_screen(fore=False)
        angle = 360
        s = "PRESS SPACE"
        b = True    # XXX WTF??
        pygame.time.set_timer(pygame.USEREVENT, 500)
        clock = pygame.time.Clock()
        while b:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == ' ':
                        b = False
            self.view.fill(bg_rgb)
            i2 = pygame.transform.rotate(self.ship, angle)
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
            angle -= 5
            angle %= 360
            clock.tick(50)
        pygame.time.set_timer(pygame.USEREVENT, 0)

    def turn(self, view, part, info):
        self.side(view.get_parent(), part, info)
        is_game_running = True
        completion_rate = 0
        player_group = pygame.sprite.GroupSingle(
            Player(view, self.font, self.ship)
        )
        balls = Balls()
        for x in range(info.getint(part, 'balls')):
            balls.add(Ball(view, self.font, info.getint(part, 'speed')))
        bg_rgb = play8.screen64_screen(fore=False)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        if pygame.mixer:
            pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while is_game_running:
            for x in pygame.event.get():
                if x.type == pygame.QUIT:
                    sys.exit()
                elif x.type == pygame.USEREVENT:
                    completion_rate += 0.017
            if completion_rate >= 1:
                is_game_running = False
            self.update_progress(view.get_parent(), completion_rate)
            player_group.sprite.move()
            if pygame.sprite.spritecollideany(player_group.sprite, balls):
                if pygame.mixer:
                    pygame.mixer.Sound(
                        os.path.join(self.path, "res", "noise_5.1.wav")
                    ).play()
                is_game_running = False
            balls.move()
            view.fill(bg_rgb)
            player_group.draw(view)
            balls.draw(view)
            pygame.display.flip()
            clock.tick(50)
        pygame.time.set_timer(pygame.USEREVENT, 0)
        if pygame.mixer:
            pygame.mixer.music.stop()
            while pygame.mixer.get_busy():
                pass
        view.fill(bg_rgb)
        pygame.display.flip()
        return completion_rate >= 1

    def update_progress(self, view, progress):
        t = 36, 1
        s = "TIME"
        play8.screen64_progress(
            self.font[2], self.font[3], progress, s.encode('ascii'), view, t
        )


class Ball(pygame.sprite.Sprite):
    "Ball"

    def __init__(self, view, font, spar):
        super().__init__()
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

    def bounce(self, spra, sprb, diff, norm):
        f = norm ** 2
        a = (numpy.dot(spra.move, diff) / f) * diff
        a2 = (numpy.dot(sprb.move, diff) / f) * diff
        spra.move += a2 - a
        sprb.move += a - a2
        return


class Player(pygame.sprite.Sprite):
    def __init__(self, view, font, ship):
        super().__init__()
        self.image = ship
        self.rect = self.image.get_rect()
        self.area = view.get_rect()
        self.rect.center = self.area.width / 2, self.area.height / 2
        pygame.mouse.set_visible(0)
        pygame.mouse.set_pos(self.rect.topleft)
        return

    def move(self):
        x, y = pygame.mouse.get_pos()
        if (
            x >= self.area.left and self.area.right >= self.rect.width + x
            and y >= self.area.top
            and self.area.bottom >= self.rect.height + y
        ):
            self.rect.left = x
            self.rect.top = y
        return
