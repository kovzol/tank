#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple tank game
written by Benedek Kovács, Domonkos Kovács
and Zoltán Kovács <zoltan@geogebra.org>
in March/April 2015

Licensed under GNU GPL 3
"""

import pygame
import random

from pygame.locals import *
from math import cos, sin, pi

level = random.randint(1,21)
earth = pygame.image.load('earth' + str(level) + '.png')
sky = pygame.image.load('sky.png')
ash = pygame.image.load('ash.png')
tank1 = pygame.image.load('tank1-nocannon.png')
cannon1 = pygame.image.load('tank1-cannon.png')
tank2 = pygame.image.load('tank2-nocannon.png')
cannon2 = pygame.image.load('tank2-cannon.png')
cannonash = pygame.image.load('cannonash.png')
ball = pygame.image.load('ball.png')
bang = pygame.image.load('bang.png')
loser = pygame.image.load('loser.png')
winner = pygame.image.load('winner.png')
draw = pygame.image.load('draw.png')

def playsound(sound):
    pygame.mixer.music.fadeout(0)
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)

def redraw(show_power, show_ball):
    global in_bang, ash_counter1, ash_counter2
    
    screen.blit(sky,(0,0))
    screen.blit(earth,(0,0))

    if show_power:
        powercolor = (33,2,227,255)
    else:
        powercolor = (0,240,255,255)
    if energy1 <= 0: 
        powercolor = (12,20,2,255)
    pygame.draw.rect(screen, powercolor, (10,10,(width-20)/10.0*power1,10), 0)

    if energy2>0:
        pygame.draw.rect(screen, (225,0,0,255), (10,25,(width-20)/100.0*energy2,10), 0)

    if energy1>0:
        pygame.draw.rect(screen, (0,105,0,255), (10,40,(width-20)/100.0*energy1,10), 0)

    if show_ball:
        screen.blit(ball, (bx, by))
    if energy1 > 0:
        screen.blit(tank1, (t1x, t1y))
        screen.blit(cannon1_rot, (c1x + c1_px, c1y + c1_py))
    if energy2 > 0:
        screen.blit(tank2, (t2x, t2y))
        screen.blit(cannon2_rot, (c2x + c2_px, c2y + c2_py))

    if in_bang > 0:
        screen.blit(bang,(int(bx)-32,int(by)-25))
        in_bang -= 1

    if energy1 <= 0:
        ash_counter1 += 1
        if ash_counter1 < 10:
            screen.blit(bang,(t1x-16,t1y-17))
        else:
            screen.blit(ash,(t1x,t1y))
            screen.blit(cannonash1_rot, (c1x + c1_px,c1y + c1_py))

    if energy2 <= 0:
        ash_counter2 += 1
        if ash_counter2 < 10:
            screen.blit(bang,(t2x-16,t2y-17))
        else:
            screen.blit(ash,(t2x,t2y))
            screen.blit(cannonash2_rot, (c2x + c2_px,c2y + c2_py))

    pygame.display.flip()

def end_loser():
    global energy1
    energy1 = 0
    redraw(False, False)
    playsound("bang.ogg")
    for i in range(1,30):
        clock.tick(100)
        redraw(False, False)
    scr = screen.copy()
    pygame.time.wait(4000)
    for i in range(0,255):
        scr_new = scr.copy()
        black = pygame.Surface((width,height)).convert_alpha()
        black.fill((0,0,0,i))
        scr_new.blit(black,(0,0))
        screen.blit(scr_new,(0,0))
        pygame.display.flip()
    if energy2 <= 0:
        screen.blit(draw,(0,0))
        font = pygame.font.SysFont("comicsansms", 60)
        text = font.render(u"Draw!", 1, (255,0,0,255))
        text_width, text_m = text.get_size() 
        where_x = width/2 - text_width/2
        where_y = height/6
        screen.blit(text, (where_x, where_y))
    else:
        screen.blit(loser,(108,0))
        playsound("laugh.mp3")
    pygame.display.flip()   
    pygame.time.wait(6000)
    exit()

def end_winner():
    scr = screen.copy()
    pygame.time.wait(4000)
    for i in range(0,255):
        scr_new = scr.copy()
        green = pygame.Surface((width,height)).convert_alpha()
        green.fill((0,255,0,i))
        scr_new.blit(green,(0,0))
        screen.blit(scr_new,(0,0))
        pygame.display.flip()
    font = pygame.font.SysFont("comicsansms", 60)
    text = font.render(u"You won!", 1, (0,0,0,255))
    text_width, text_m = text.get_size() 
    where_x = width/2 - text_width/2
    where_y = height/2 - text_m/2
    screen.blit(winner, (width/2-100,height-250))
    screen.blit(text, (where_x, 50))
    pygame.display.flip()
    pygame.time.wait(8000)
    exit()

def tanks_up_down():
    """Move the tanks up or down depending on falling or lifting up."""
    global t1y, c1y, energy1, t2y, c2y, energy2
    tankheight = 16
    row_below_tank1 = t1y + tankheight
    row_below_tank2 = t2y + tankheight
    # Falling down:
    falling1 = 0
    falling2 = 0
    while ((row_below_tank1 < height + 2*tankheight) and only_sky_in_row1(row_below_tank1)) or ((row_below_tank2 < height + 2*tankheight) and only_sky_in_row2(row_below_tank2)):
       
        if only_sky_in_row1(row_below_tank1) and row_below_tank1 < height + 2*tankheight:
            t1y += 1
            c1y += 1
            falling1 += 1
            if falling1 > 5:
                energy1 -= 3
            row_below_tank1 += 1
            
        if only_sky_in_row2(row_below_tank2) and row_below_tank2 < height + 2*tankheight:
            t2y += 1
            c2y += 1
            falling2 += 1
            if falling2 > 5:
                energy2 -= 3
            row_below_tank2 += 1

        redraw(False, False)
    if row_below_tank1 >= height + 2*tankheight:
        if row_below_tank2 >= height + 2*tankheight:
            energy2 = 0 # draw!
        end_loser()
    if row_below_tank2 >= height + 2*tankheight:
        end_winner()

    may_lift_up = 4
    tank1_last_row = row_below_tank1 - 1
    while may_lift_up >= 0:
        may_lift_up -= 1
        while not only_sky_in_row1(tank1_last_row):
            t1y -= 1
            c1y -= 1
            tank1_last_row -= 1
            redraw(False, False)

def only_sky_in_row1(row):
    """Checks if there is only sky about below tank1"""
    sky_counter = 0
    for i in range(8,24):
        if is_earth(t1x+i,row):
            sky_counter += 1
    if sky_counter > 2:
        return False
    return True

def only_sky_in_row2(row):
    """Checks if there is only sky about below tank2"""
    sky_counter = 0
    for i in range(8,24):
        if is_earth(t2x+i,row):
            sky_counter += 1
    if sky_counter > 2:
        return False
    return True

def only_earth_in_row1(row):
    """Checks if there is only earth about below tank1"""
    answer = True # assume yes, and if we find a sky pixel, this will be False (i.e., no)
    for i in range(8,24):
        if not is_earth(t1x+i,row):
            answer = False
    return answer

def only_sky_in_column(column):
    """Checks if in a column about tank1 about its bottom (but not totally bottom) there is only sky"""
    answer = True # assume yes, and if we find an earth pixel, this will be False (i.e., no)
    for i in range(0,5):
        if is_earth(column,t1y+i):
            answer = False
    return answer

def on_screen(x,y):
    if x<0 or y<0 or x>=width or y>=height:
        return False
    return True

def is_earth(x,y):
    if not on_screen(x,y):
        return False
    earth_color = earth.get_at((int(x),int(y)))
    if earth_color == (255,255,255,0):
        return False
    return True 

def show_bang(x,y):
    for i in range(0,17):
        pygame.draw.circle(earth, (255,255,255,0), (x,y),i, 0) # hole
        tanks_up_down()
        redraw(False, False)

def cannon2_rotate():
    global cannon2_rot, c2_px, c2_py, cannonash2_rot
    cannon2_rot = pygame.transform.rotate(cannon2, rot2)
    cannonash2_rot = pygame.transform.rotate(cannonash, rot2)
    cannon2_rot.get_rect().center = (c2x + 16, c2y + 16)
    cannonash2_rot.get_rect().center = (c2x + 16, c2y + 16)
    cannon2_rot_size = cannon2_rot.get_size()
    cannon2_rot_width = cannon2_rot_size[0]
    cannon2_rot_height = cannon2_rot_size[1]
    c2_px = (33 - cannon2_rot_width)/2
    c2_py = (33 - cannon2_rot_height)/2 + sin(rot2 / 180.0 * pi) * 5 + 1

def is_hit1():
    """
    If the center of the tank is closer than 8 pixels from the center of the ball, then
    there is a hit. The ball is of 6x6 size, the tank is 32x16.
    """
    tank_center_x = t1x + 16
    tank_center_y = t1y + 8
    ball_center_x = bx + 3
    ball_center_y = by + 3
    if (tank_center_x - ball_center_x)**2 + (tank_center_y - ball_center_y)**2 <= 8**2:
        return True
    return False 

def is_hit2():
    tank_center_x = t2x + 16
    tank_center_y = t2y + 8
    ball_center_x = bx + 3
    ball_center_y = by + 3
    if (tank_center_x - ball_center_x)**2 + (tank_center_y - ball_center_y)**2 <= 8**2:
        return True
    return False 

def ball_shoot():
    global bx, by, bsy, in_bang, energy1, energy2
    playsound("shoot.ogg")
    pygame.time.wait(100)
    while (on_screen(bx, by) or by<0) and not is_earth(bx, by) and not is_hit1() and not is_hit2():
        redraw(False, True)
        bx += bsx 
        by += bsy
        bsy += 0.1
        clock.tick(100)
    if on_screen(bx, by) and (is_earth(bx, by) or is_hit1() or is_hit2()):
        # Bang:
        in_bang = 10
        playsound("bang.ogg")
        show_bang(int(bx),int(by))
        if is_hit1():
            energy1 -= 10
        if is_hit2():
            energy2 -= 10
        tanks_up_down()

def do_nothing():
    """Wait a little bit, do nothing. If there is something to draw meanwhile (e.g. ash), it will also be drawn."""
    for i in range(0,50):
        redraw(False, False)
        clock.tick(100)

def test(r, p):
    """Tests what should happen if tank2 would shoot by using rotation r and power p."""
    global bx, by
    bx = t2x + 15 + cos(r / 180.0 * pi) * 10
    by = t2y - sin(r / 180.0 * pi) * 10
    bsx = cos(r / 180.0 * pi) * p
    bsy = - sin(r / 180.0 * pi) * p
    while (on_screen(bx, by) or by<0) and not is_earth(bx, by) and not is_hit1() and not is_hit2():
        bx += bsx
        by += bsy
        bsy += 0.1
    # print bx, by, r, p, is_hit1()
    return is_hit1()

# SETTINGS ON GAME STARTUP

width = 640
height = 400
screen = pygame.display.set_mode((width, height))
running = 1

# Position of the tanks
t1x = width / 6 + random.randint(0, int(width/6))
t1y = 0
while only_sky_in_row1(t1y + 16) and t1y + 16 < height:
    t1y += 1
t2x = width / 6 * 4 + random.randint(0,int(width/6))
t2y = 0
while only_sky_in_row2(t2y + 16)  and t2y + 16 < height:
    t2y += 1

# Position of the cannons
c1x = t1x - 1
c1y = t1y - 14
c2x = t2x - 1
c2y = t2y - 14

rot1 = 0
rot2 = 180

power1 = 5

energy1 = 100
energy2 = 100

old_k_delay, old_k_interval = pygame.key.get_repeat()
pygame.key.set_repeat(500, 30)

clock = pygame.time.Clock()
clock.tick()

pygame.init()

in_bang = 0
ash_counter1 = 0
ash_counter2 = 0

# Game difficulty
diff = random.randint(1,3)
if diff == 3:
    no_attempts = 1000
    difftext = u"hard"
if diff == 2:
    no_attempts = 20
    difftext = u"medium"
if diff == 1:
    no_attempts = 5
    difftext = u"easy"
font = pygame.font.SysFont("comicsansms", 30)
text = font.render(u"The game will be " + difftext + " now!", 1, (255,255,255,255))
text_width, text_height = text.get_size()
where_x = width/2 - text_width/2
where_y = height/2 - text_height/2
screen.blit(text, (where_x, where_y))
pygame.display.flip()
pygame.time.wait(1000)


while running:

    cannon1_rot = pygame.transform.rotate(cannon1, rot1)
    cannonash1_rot = pygame.transform.rotate(cannonash, rot1)
    cannon1_rot.get_rect().center = (c1x + 16, c2y + 16)
    cannonash1_rot.get_rect().center = (c1x + 16, c2y + 16)
    cannon1_rot_size = cannon1_rot.get_size()
    cannon1_rot_width = cannon1_rot_size[0]
    cannon1_rot_height = cannon1_rot_size[1]
    c1_px = (33 - cannon1_rot_width)/2
    c1_py = (33 - cannon1_rot_height)/2 + sin(rot1 / 180.0 * pi) * 5 + 1

    cannon2_rotate()

    redraw(True, False)

    events = pygame.event.get()

    for e in events:
        if energy1 <= 0:
            end_loser()

        if e.type == pygame.KEYDOWN:
            if e.key == K_UP and rot1 < 180:
                rot1 = rot1 + 5
            if e.key == K_DOWN and rot1 > 0:
                rot1 = rot1 - 5
            if e.key == K_LEFT and t1x>0 and only_sky_in_column(t1x-1):
                t1x -= 7 #1
                c1x -= 7 #1
                tanks_up_down() 
            if e.key == K_RIGHT and t1x<width-32 and only_sky_in_column(t1x+32):
                t1x += 7 #1
                c1x += 7 #1
                tanks_up_down() 
            if e.key == K_LCTRL and power1 > 2:
                power1 -= 1
            if e.key == K_LALT and power1 < 10:
                power1 += 1
            if e.key == K_SPACE:
                # Tank 1 shoots
                bx = t1x + 15 + cos(rot1 / 180.0 * pi) * 10
                by = t1y - sin(rot1 / 180.0 * pi) * 10
                bsx = cos(rot1 / 180.0 * pi) * power1
                bsy = - sin(rot1 / 180.0 * pi) * power1
                ball_shoot()
                if energy2 <= 0:
                    do_nothing()
                    end_winner()
                # Now tank 2 shoots (if he still lives)
                if energy2 > 0:
                    pygame.time.wait(500)
                    # 1. He hecks the direction (left or right to tank 1)
                    attempts = 0
                    should_hit = False

                    while attempts < no_attempts and not should_hit:#100
                        if t1x < t2x:
                            # Tank 1 is left to tank 2.
                            planned_angle = random.randint(90,180)
                        else:
                            planned_angle = random.randint(0,90)
                        # Power is computed based on the distance
                        power2 = int(abs(t2x-t1x)/50) + random.randint(0,4) - 2
                        if power2 > 10:
                            power2 = 10
                        if power2 < 1:
                            power2 = 1
                        should_hit = test(planned_angle, power2)
                        attempts += 1

                    while rot2 != planned_angle:
                        if rot2 < planned_angle:
                            rot2 += 1
                        else:
                            rot2 -= 1
                        cannon2_rotate()
                        redraw(False, False)
                        clock.tick(100)
                    # 2. Shooting
                    bx = t2x + 15 + cos(rot2 / 180.0 * pi) * 10
                    by = t2y - sin(rot2 / 180.0 * pi) * 10
                    bsx = cos(rot2 / 180.0 * pi) * power2
                    bsy = - sin(rot2 / 180.0 * pi) * power2
                    ball_shoot()
                    if energy2 <= 0:
                        do_nothing()
                        end_winner()

        if e.type == pygame.QUIT:
            pygame.key.set_repeat(old_k_delay, old_k_interval)
            running = False

    clock.tick(30)

