import pygame
from pygame import *
pygame.init()
from math import ceil

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, im_x, im_y, x, y, speed):
        super().__init__()

        self.image = transform.scale(image.load(pl_image), (im_x, im_y))
        self.pl_image = pl_image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.x = x+1
        self.y = y+1
        self.rect.x = 22+81*x
        self.rect.y = 580-78*y
        self.queen = False

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class White(GameSprite):
    def move(self, x, y):
        self.rect.x = 22+81*(x-1)
        self.rect.y = 580-78*(y-1)


class Black(GameSprite):
    def move(self, x, y):
        self.rect.x = 22+81*(x-1)
        self.rect.y = 580-78*(y-1)

class Step(GameSprite):
    def f(self):
        self.rect.x += 12
        self.rect.y += 12
    
    def  m(self,x,y):
        self.rect.x = 22+81*(x-1) + 12
        self.rect.y = 580-78*(y-1) + 12

class Kill_step(GameSprite):
    def __init__(self, pl_image, im_x, im_y, x, y):
        #super().__init__()

        self.image = transform.scale(image.load(pl_image), (im_x, im_y))
        self.pl_image = pl_image
        self.rect = self.image.get_rect()
        self.x = x+1
        self.y = y+1
        self.rect.x = 22+81*x
        self.rect.y = 580-78*y
        self.direction = "UR"

    def f(self):
        self.rect.x += 12
        self.rect.y += 12
    
    def  m(self,x,y):
        self.rect.x = 22+81*(x-1) + 12
        self.rect.y = 580-78*(y-1) + 12

wx = 686
wy = 686
window = display.set_mode((wx,wy))
display.set_caption("Шутер")
background = transform.scale(image.load("Поле.jpg"), (wx,wy))
font = font.Font(None,60)

wc = []
bc = []
steps = []
kill_steps = []

for i in range(3):
    for j in range(4):
        white_checker = White('Белая шашка.png',75,75,2*j+i%2,i,5)
        wc.append(white_checker)

for i in range(3):
    for j in range(4):
        black_checker = Black('Чёрная шашка.png',75,75,2*j-i%2+1,i+5,5)
        bc.append(black_checker)

for i in range(8):
    for j in range(4):
        step = Step('Ход.png',50,50,2*j+i%2,i,5)
        step.f()
        steps.append(step)

for i in range(8):
    for j in range(4):
        kill_step = Kill_step('Убийственный ход.png',50,50,2*j+i%2,i)
        kill_step.f()
        kill_steps.append(kill_step)

step = "White"
checker = 0
UR_kill_checker = 0
UL_kill_checker = 0
DR_kill_checker = 0
DL_kill_checker = 0
coordinates = []
for i in range(8):
    coordinates.append([])
for i in range(8):
    for j in range(4):
        coordinates[i].append("N")

for i in range(12):
    coordinates[wc[i].y-1][ceil(wc[i].x/2)-1] = "White"
for i in range(8):
    coordinates[wc[i].y+2][ceil(wc[i].x/2)-1] = "Nothing"
for i in range(12):
    coordinates[wc[i].y+4][ceil(wc[i].x/2)-1] = "Black"
print(coordinates)
clock = time.Clock()

game = True
finish = False
while game:
    window.blit(background, (0,0))

    for i in wc:
        i.update()
    for i in bc:
        i.update()
    for i in range(32):
        steps[i].m(-100,-100)
    for i in range(32):
        kill_steps[i].m(-100,-100)
    for i in range(32):
        if coordinates[int(i/4)][i%4] == "Step":
            y = int(i/4) + 1
            x = i%4*2 - y%2 + 2
            steps[i].m(x, y)
            steps[i].update()
    for i in range(32):
        c = coordinates[int(i/4)][i%4]
        if c == "UR_kill_step" or c == 'UL_kill_step' or c == 'DR_kill_step' or c == 'DL_kill_step':
            y = int(i/4) + 1
            x = i%4*2 - y%2 + 2
            kill_steps[i].m(x, y)
            kill_steps[i].update()
        if c == "UR_kill_step":
            kill_steps[i].direction = 'UR'
        if c == "UL_kill_step":
            kill_steps[i].direction = 'UL'
        if c == "DR_kill_step":
            kill_steps[i].direction = 'DR'
        if c == "DL_kill_step":
            kill_steps[i].direction = 'DL'

    coordinates2 = []
    for i in coordinates:
        coordinates2.append(i)
    
    #Отображение кружков ходов:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            for i in range(32):
                c = coordinates[int(i/4)][i%4]
                if c == "Step" or c == "UR_kill_step" or c == 'UL_kill_step' or c == 'DR_kill_step' or c == 'DL_kill_step':
                    coordinates[int(i/4)][i%4] = "Nothing"
            if step == 'White': #Белые
                for j in range(len(wc)):
                    pos = mouse.get_pos()
                    i = wc[j]
                    if i.rect.collidepoint(pos):
                        if i.queen == 0:
                            if i.y % 2 == 1:
                                checker = j
                                if i.x == 1:
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                    UR_kill_checker = k
                                elif i.x == 7:
                                    if coordinates[i.y][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-2] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = 'UL_kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                    UL_kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-2] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                    UL_kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                    UR_kill_checker = k
                            else:
                                checker = j
                                if i.x == 8:
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                UL_kill_checker = k
                                elif i.x == 2:
                                    if coordinates[i.y][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)] == 'Black' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)] = 'UR_kill_step'
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                UR_kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                UL_kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)] == 'Black' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                UR_kill_checker = k
                            if i.y != 1 and i.y != 2:
                                checker = j
                                if i.y % 2 == 1:
                                    if i.x == 1:
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothnig":
                                            coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    DR_kill_checker = k
                                    elif i.x == 7:
                                        if coordinates[i.y-2][ceil(i.x/2)-2] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                    else:
                                        if coordinates[i.y-2][ceil(i.x/2)-2] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = 'DL_kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = 'DR_kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    DR_kill_checker = k
                                else:
                                    checker = j
                                    if i.x == 8:
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black"and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                    elif i.x == 2:
                                        if coordinates[i.y-2][ceil(i.x/2)] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    DR_kill_checker = k
                                    else:
                                        if coordinates[i.y-2][ceil(i.x/2)] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    DR_kill_checker = k
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                        

                        else:
                            checker = j

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x < 8 and y < 8:
                                x += 1
                                y += 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "UR_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "Black":
                                    if kill == 0:
                                        kill = 1
                                        for k in range(len(bc)):
                                            if bc[k].y == y and bc[k].x == x:
                                                UR_kill_checker = k
                                    else:
                                        end = 1
                                else:
                                    end = 1

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x < 8 and y > 1:
                                x += 1
                                y -= 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "DR_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "Black":
                                    if kill == 0:
                                        kill = 1
                                        for k in range(len(bc)):
                                            if bc[k].y == y and bc[k].x == x:
                                                DR_kill_checker = k
                                    else:
                                        end = 1
                                else:
                                    end = 1

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x > 1 and y > 1:
                                x -= 1
                                y -= 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "DL_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "Black":
                                    if kill == 0:
                                        kill = 1
                                        for k in range(len(bc)):
                                            if bc[k].y == y and bc[k].x == x:
                                                DL_kill_checker = k
                                    else:
                                        end = 1
                                else:
                                    end = 1
                            
                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x > 1 and y < 8:
                                x -= 1
                                y += 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "UL_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "Black":
                                    if kill == 0:
                                        kill = 1
                                        for k in range(len(bc)):
                                            if bc[k].y == y and bc[k].x == x:
                                                UL_kill_checker = k
                                    else:
                                        end = 1
                                else:
                                    end = 1

                                
                        print(coordinates)
            else: #Чёрные
                for j in range(len(bc)):
                    pos = mouse.get_pos()
                    i = bc[j]
                    if i.rect.collidepoint(pos):
                        if i.queen == 0:
                            if i.y % 2 == 1:
                                checker = j
                                if i.x == 1:
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                DR_kill_checker = k
                                elif i.x == 7:
                                    if coordinates[i.y-2][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-2] == "White" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                DL_kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y-2][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-2] == "White" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)-2] = 'DL_kill_step'
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                DL_kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)] = 'DR_kill_step'
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                DR_kill_checker = k
                            else:
                                checker = j
                                if i.x == 8:
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                elif i.x == 2:
                                    if coordinates[i.y-2][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                    DR_kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "DL_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                    DL_kill_checker = k
                                                    print(k)
                                                    print('dkfjlksdjf')
                                    if coordinates[i.y-2][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "DR_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                    DR_kill_checker = k
                            if i.y != 7 and i.y != 8:
                                checker = j
                                if i.y % 2 == 1:
                                    if i.x == 1:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    UR_kill_checker = k
                                    if i.x == 7:
                                        if coordinates[i.y][ceil(i.x/2)-2] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = 'UL_kill_step'
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    UL_kill_checker = k
                                    else:
                                        if coordinates[i.y][ceil(i.x/2)-2] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    UL_kill_checker = k
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'While' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    UR_kill_checker = k
                                else:
                                    if i.x == 8:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                            for k in range(len(wc)):
                                                    if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                        UL_kill_checker = k
                                    elif i.x == 2:
                                        if coordinates[i.y][ceil(i.x/2)] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = 'UR_kill_step'
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    UR_kill_checker = k
                                    else:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "UL_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    UL_kill_checker = k
                                        if coordinates[i.y][ceil(i.x/2)] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "UR_kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    UR_kill_checker = k

                        else:
                            checker = j

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x < 8 and y < 8:
                                x += 1
                                y += 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "UR_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "White":
                                    kill = 1
                                    for k in range(len(wc)):
                                        if wc[k].y == y and wc[k].x == x:
                                            UR_kill_checker = k
                                else:
                                    end = 1

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x < 8 and y > 1:
                                x += 1
                                y -= 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "DR_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "White":
                                    kill = 1
                                    for k in range(len(wc)):
                                        if wc[k].y == y and wc[k].x == x:
                                            DR_kill_checker = k
                                else:
                                    end = 1

                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x > 1 and y > 1:
                                x -= 1
                                y -= 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "DL_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "White":
                                    kill = 1
                                    for k in range(len(wc)):
                                        if wc[k].y == y and wc[k].x == x:
                                            DL_kill_checker = k
                                else:
                                    end = 1
                            
                            end = 0
                            kill = 0
                            x = i.x
                            y = i.y
                            while end == 0 and x > 1 and y < 8:
                                x -= 1
                                y += 1
                                if coordinates[y-1][ceil(x/2)-1] == "Nothing":
                                    if kill == 0:
                                        coordinates[y-1][ceil(x/2)-1] = "Step"
                                    else:
                                        coordinates[y-1][ceil(x/2)-1] = "UL_kill_step"
                                elif coordinates[y-1][ceil(x/2)-1] == "White":
                                    kill = 1
                                    for k in range(len(wc)):
                                        if wc[k].y == y and wc[k].x == x:
                                            UL_kill_checker = k
                                else:
                                    end = 1
                        print(coordinates)
            
            #Хождение:
            for i in steps:
                pos = mouse.get_pos()
                if i.rect.collidepoint(pos):
                    if step == "White":
                        step = 'Black'
                        coordinates[wc[checker].y-1][ceil(wc[checker].x/2)-1] = 'Nothing'
                        wc[checker].move(i.x,i.y)
                        wc[checker].y = i.y
                        wc[checker].x = i.x
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'White'
                        if wc[checker].y == 8:
                            wc[checker].queen = 1
                        print(coordinates)
                        break
                    else:
                        step = 'White'
                        coordinates[bc[checker].y-1][ceil(bc[checker].x/2)-1] = 'Nothing'
                        bc[checker].move(i.x,i.y)
                        bc[checker].y = i.y
                        bc[checker].x = i.x
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'Black'
                        if bc[checker].y == 1:
                            bc[checker].queen = 1
                        print(coordinates)
                        break
                
            for i in kill_steps:
                pos = mouse.get_pos()
                if i.rect.collidepoint(pos):
                    if step == "White":
                        if i.direction == 'UR':
                            kc = UR_kill_checker
                        if i.direction == 'UL':
                            kc = UL_kill_checker
                        if i.direction == 'DR':
                            kc = DR_kill_checker
                        if i.direction == 'DL':
                            kc = DL_kill_checker
                        step = 'Black'
                        coordinates[wc[checker].y-1][ceil(wc[checker].x/2)-1] = 'Nothing'
                        wc[checker].move(i.x,i.y)
                        wc[checker].y = i.y
                        wc[checker].x = i.x
                        coordinates[bc[kc].y-1][ceil(bc[kc].x/2)-1] = "Nothing"
                        del bc[kc]
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'White'
                        if wc[checker].y == 8:
                            wc[checker].queen = 1
                        print(coordinates)
                        break
                    else:
                        if i.direction == 'UR':
                            kc = UR_kill_checker
                        if i.direction == 'UL':
                            kc = UL_kill_checker
                        if i.direction == 'DR':
                            kc = DR_kill_checker
                        if i.direction == 'DL':
                            kc = DL_kill_checker
                        print(kc)
                        step = 'White'
                        coordinates[bc[checker].y-1][ceil(bc[checker].x/2)-1] = 'Nothing'
                        bc[checker].move(i.x,i.y)
                        bc[checker].y = i.y
                        bc[checker].x = i.x
                        coordinates[wc[kc].y-1][ceil(wc[kc].x/2)-1] = "Nothing"
                        del wc[kc]
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'Black'
                        if wc[checker].y == 8:
                            wc[checker].queen = 1
                        print(coordinates)
                        break
                    

        

        
        if e.type == QUIT:
            game = False

    if coordinates2 != coordinates:
        print(coordinates)

    if len(wc) == 0:
        WHITE_WIN = font.render('Белые выиграли', True, (0,255,40))
        window.blit(WHITE_WIN, (165, 300))
    if len(bc) == 0:
        BLACK_WIN = font.render('Чёрные выиграли', True, (0,255,40))
        window.blit(BLACK_WIN, (155, 300))
    clock.tick(60)
    display.update()
