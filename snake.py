# Snake Tutorial Python
# Learn Python by Building Five Games - Full Course
# freeCodeCamp.org
# https://www.youtube.com/watch?v=XGf2GcyHPhc&t=2668s
#

import turtle
#  from turtle import Turtle
#  import time
import os  # System Operating System to add sound

#  import math
import random
import pygame

wn = turtle.Screen()
wn.title("Snake!")
wn.bgcolor("white")
wn.setup(width=500, height=100, starty=150)
wn.tracer()  # Stops window from updating


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]  # Row X
        j = self.pos[1]  # Col Y
        
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circle_middle = (i * dis + center - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0  # Direction for x -1/0/1 -> 0 means the other coordinate is moving
        self.dirny = 1  # Direction for y -1/0/1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.system("killall afplay")
                pygame.quit()
                exit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_x]:
                    os.system("killall afplay")
                    pygame.display.quit()
                    pygame.quit()
                    exit()

                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)

                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        added = False
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
            added = True
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
            added = True
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
            added = True
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
            added = True

        if added:
            os.system("afplay yum.wav&")
            message_box0("Your Snakes is now " + str(len(s.body)) + " Long!", " E(x)it")

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    size_btwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += size_btwn
        y += size_btwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # Don't place snack on snake
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    # pen
    global play_again
    play_again = False
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("black")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, -20)
    pen0.clear()
    os.system("killall afplay")
    os.system("afplay GameOver.mp3&")
    pen.write(f"{subject}{content}", align="center",
              font=("Courier", 16, "normal"))
    while not play_again:
        wn.update()
        pygame.display.update()
    pen.clear()
    message_box0("GOOD MUNCHING!!!", "")
    pygame.display.set_mode((width, width))
    os.system("afplay HareNet.mp3&")


def message_box0(subject, content):
    # pen
    global play_again, pen0
    pen0.clear()
    pen0.write(f"{subject}{content}", align="center", font=("Courier", 16, "normal"))

#    input("Play Again")


def play_again():
    global play_again
    play_again = True


wn.listen()  # Listen for keyboard input

wn.onkeypress(play_again, "space")  # when user enters spacebar, call function paddle_a_up


def main():
    global width, rows, s, snack
    width = 500
    rows = 20  # Should divide evenly into height
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    os.system("afplay HareNet.mp3&")

    while flag:
        pygame.time.delay(50)  # Effects the speed of the game - Lower is Faster
        clock.tick(10)  # The Lower the Slower
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color=(0, 255, 0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box("Game Over! Your Snakes was " + str(len(s.body)) + " Long!",
                            "\n   To play again click here then\n          Press Enter")
                s.reset((10, 10))
                break

        redraw_window(win)


play_again = False

pen0 = turtle.Turtle()
pen0.speed(0)
pen0.color("black")
pen0.penup()
pen0.hideturtle()
pen0.goto(0, -10)

message_box0("GOOD MUNCHING!!!", "")

main()
