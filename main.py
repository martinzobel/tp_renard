from random import randint
import pygame as pg
import numpy as np
import random as rd

pg.init()
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()
white = (255,255,255)
black = (0,0,0)
brown = (101, 67, 33)
orange = (255,165,0)
red = (255,0,0)

k = 0
direction = (0,0)
dir = None
running = True
begin = False
# begin est le booléen qui indique quand la partie à commencé
# dir va permettre de continuer à avancer dans la direction précédente tant qu'aucune direction nouvelle n'a été donnée

class Lapin:
    def __init__(self):
        self.x = 15
        self.y = 15
    def move(self,direction):
        self.x+= direction[0]
        self.y+= direction[1]

class Piege:
    def __init__(self):
        self.L = []
    def add(self,x,y):
        self.L.append((x,y))

class Renard:
    def __init__(self):
        self.L = []
        self.score = 0
    def add(self):
        x,y = rd.randint(0,30),rd.randint(0,30)
        while (x,y) in self.L or (x,y) in Pg.L or (x,y) == (Lp.x, Lp.y):
            x,y = rd.randint(0,30),rd.randint(0,30)
        self.L.append((x,y))
    def move(self,x,y):
        for i in range(len(self.L)) :
            r = self.L[i]
            if abs(x-r[0])>abs(y-r[1]):
                if x>r[0]:
                    self.L[i] = (r[0]+1,r[1])
                else:
                    self.L[i] = (r[0]-1,r[1])
            else:
                if y>r[1]:
                    self.L[i] = (r[0],r[1]+1)
                else:
                    self.L[i] = (r[0],r[1]-1)
    def capture(self,x,y):
        while (x,y) in self.L:
            self.L.remove((x,y))
            self.score+=1

Lp = Lapin()
Rd = Renard()
Pg = Piege()

while running:
    clock.tick(2)
    pg.display.set_caption(f"Score: {Rd.score}")

    #Affichage du plateau
    for i in range(30):
            for j in range(30):
                x,y = i*20,j*20
                rect = pg.Rect(x,y,20,20)
                if (i+j)%2 ==0:
                    pg.draw.rect(screen, white, rect)
                else:
                    pg.draw.rect(screen, black, rect)
    #Affichage du Lapin:
    x,y = Lp.x,Lp.y
    rect = pg.Rect(x*20,y*20,20,20)
    pg.draw.rect(screen, brown, rect)

    #Affichage des pièges:
    for v in Pg.L:
        rect = pg.Rect(v[0]*20,v[1]*20,20,20)
        pg.draw.rect(screen, red, rect)

    #Affichage des renards:
    for v in Rd.L:
        rect = pg.Rect(v[0]*20,v[1]*20,20,20)
        pg.draw.rect(screen, orange, rect)
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            running = False
        
        elif event.type == pg.KEYDOWN:
            begin = True
            if event.key == pg.K_q:
                running = False

            elif event.key == pg.K_DOWN and dir != 'DOWN':
                direction = (0,1)
                dir = 'DOWN'
            elif event.key == pg.K_UP and dir !='UP':
                direction = (0,-1)
                dir = 'UP'
            elif event.key == pg.K_RIGHT and dir !='RIGHT':
                direction = (1,0)
                dir = 'RIGHT'
            elif event.key == pg.K_LEFT and dir !='LEFT':
                direction = (-1,0)
                dir = 'LEFT'
            
            elif event.key == pg.K_SPACE:
                x,y = Lp.x,Lp.y
                Pg.add(x,y)
            break # Sans ça il y avait un délai 

    if begin :
        #Déplacement du lapin (si il ne rencontre ni un renard ni un piège et qu'il ne sort pas du cadre)
        xnew,ynew=Lp.x+direction[0],Lp.y+direction[1]
        if (xnew,ynew) in Pg.L or (xnew,ynew) in Rd.L:
            running = False
        elif xnew >= 30 or xnew<0 or ynew >= 30 or ynew<0:
            running = False
        elif begin:
            Lp.x = xnew
            Lp.y = ynew

        #Supression des renards sur un piege puis supression du piege:
        for (x,y) in Pg.L:
            if (x,y) in Rd.L:
                Rd.capture(x,y)

        #Déplacement des renards
        Rd.move(Lp.x,Lp.y)
        if (Lp.x,Lp.y) in Rd.L:
            running = False
    
        #Ajout d'un renard
        if k%10 ==0:
            Rd.add()
        k+=1
        
    pg.display.update()

pg.quit()