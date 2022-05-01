import random as rnd
import pygame
import pygame_gui
import time
from os.path import exists
from datetime import datetime
import pickle

#initialising the game
pygame.init()

X = 416
Y = 416
pygame.display.set_caption("Labyrinthine")
window_surface = pygame.display.set_mode((X, Y))
manager = pygame_gui.UIManager((X, Y), "GUI/button_test.json")

bg = pygame.image.load("GUI/LAB.jpg")
window_surface.blit(bg, (0, 0))

feed_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 200), (50, 50)),
                                            text="",
                                            manager=manager)

life_bar = pygame_gui.elements.ui_status_bar.UIStatusBar(relative_rect=pygame.Rect((20, 20), (100, 20)),
                                                         manager=manager)
#generate a random 8x8 tile of 0s and 1s
def spr_gen(sym): #pass kind of symmetry
    spr = ""
    if sym==1: #bilateral
        for _ in range(8):
            tspr = ""
            for _ in range(4):
                tspr += str(rnd.randint(0,1))
            spr += tspr + tspr[::-1] + "\n"
        return spr
    elif sym==2: #radial
        for _ in range(4):
            tspr = ""
            for _ in range(4):
                tspr += str(rnd.randint(0,1))
            spr += tspr + tspr[::-1] + "\n"
            ass=spr[::-1]
        spr += ass[1:] + "\n"
        return spr
    else: #random
        for _ in range(8):
            for _ in range(8):
                spr += str(rnd.randint(0,1))
            spr += "\n"
        return spr

def save():
    saveGame = open('SAVE/savegame.dat', 'wb')
    saveValues = (life, datetime.now())
    pickle.dump(saveValues, saveGame)
    saveGame.close()

def load():
    loadGame = open('SAVE/savegame.dat', 'rb')
    loadValues = pickle.load(loadGame)
    life = loadValues[0]
    last = loadValues[1]
    # location = loadValues[2]
    loadGame.close()
    return life, last

is_running = True
clock = pygame.time.Clock()
#load game here/set life
life_max = 100
life_min = 0.01
if exists('SAVE/savegame.dat'):
    life, last = load()
    life -= (datetime.now()-last).total_seconds()*.001
else:
    life = life_max #LAB's lifeforce

while is_running:
    time_delta = clock.tick(60)/1000.0
    life -= time_delta*.02
    life_bar.percent_full = life
    if life > life_max:
        life = life_max
    elif life < life_min:
        life = life_min

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save() #save game here
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == feed_button:
                # generate and save bitsy world
                f = open("OUT/" + str(time.time()) + ".bitsy", "x")
                #World name generator?

                #Header
                f.write("Write your game's title here\n\n# BITSY VERSION 7.12\n\n! ROOM_FORMAT 1\n\n")

                #Palette
                pal = ""
                for _ in range(3):
                    for i in range(3):
                        pal += str(rnd.randint(0,round(255*(life/life_max))))
                        if i==2: 
                            pal += "\n"
                        else:
                            pal += ","
                f.write("PAL 0\nNAME blueprint\n" + pal +"\n")


                #Tile
                tname = "a"
                tile = spr_gen(rnd.randint(0,round(2*(life/life_max))))

                #Avatar
                avatar = spr_gen(rnd.randint(0,round(2*(life/life_max))))

                #Sprite
                sprite = spr_gen(rnd.randint(0,round(2*(life/life_max))))
                #Dialog generator for the sprite?

                #Room
                dns = rnd.randint(1,round(5*(life/life_max))) #tile density in room/bigger number=lower density
                room = ""
                for _ in range(16):
                    for i in range(16):
                        if rnd.randint(0,dns)==dns:
                            room += tname
                        else:
                            room += "0"
                        if i==15: 
                            room += "\n"
                        else:
                            room += ","
                
                f.write("ROOM 0\n" + room + "NAME example room\nPAL 0\n\n")
                f.write("TIL " + tname + "\n" + tile + "NAME block\n\n")
                f.write("SPR A" + "\n" + avatar + "POS 0 4,4\n\n")
                f.write("SPR a" + "\n" + sprite + "NAME cat\nDLG 0\nPOS 0 8,12\n\n")

                f.close()
                
                life += 1

                print('Labyrinthine has fed!')
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(bg, (0, 0))
    # font = pygame.font.Font(None, 18)
    # text = font.render('Life: ' + str(round(life, 1)), True, (255, 255, 255))
    # textRect = text.get_rect()
    # textRect.center = (110, 50)
    # window_surface.blit(text, textRect)
    manager.draw_ui(window_surface)
    pygame.display.update()
