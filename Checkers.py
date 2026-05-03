from pygame import *
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
        kill_step = Kill_step('Убийственный ход.png',50,50,2*j+i%2,i,5)
        kill_step.f()
        kill_steps.append(kill_step)

step = "White"
checker = 0
kill_schekcer = 0
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
        if coordinates[int(i/4)][i%4] == "Kill_step":
            y = int(i/4) + 1
            x = i%4*2 - y%2 + 2
            kill_steps[i].m(x, y)
            kill_steps[i].update()

    coordinates2 = []
    for i in coordinates:
        coordinates2.append(i)
    
    #Отображение кружков ходов:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            for i in range(32):
                if coordinates[int(i/4)][i%4] == "Step" or coordinates[int(i/4)][i%4] == "Kill_step":
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
                                            coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                                elif i.x == 7:
                                    if coordinates[i.y][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-2] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = 'Kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-2] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and i.y != 7:
                                        if coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                            else:
                                checker = j
                                if i.x == 8:
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                        for k in range(len(bc)):
                                                if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                elif i.x == 2:
                                    if coordinates[i.y][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)] == 'Black' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)] = 'Kill_step'
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y][ceil(i.x/2)-1] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)-1] == 'Black' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x-1:
                                                kill_checker = k
                                    if coordinates[i.y][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y][ceil(i.x/2)] == 'Black' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                        coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                        for k in range(len(bc)):
                                            if bc[k].y == i.y+1 and bc[k].x == i.x+1:
                                                kill_checker = k
                            if i.y != 1 and i.y != 2:
                                checker = j
                                if i.y % 2 == 1:
                                    if i.x == 1:
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothnig":
                                            coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                                    elif i.x == 7:
                                        if coordinates[i.y-2][ceil(i.x/2)-2] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                    else:
                                        if coordinates[i.y-2][ceil(i.x/2)-2] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = 'Kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = 'Kill_step'
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                                else:
                                    checker = j
                                    if i.x == 8:
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black"and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                    if i.x == 2:
                                        if coordinates[i.y-2][ceil(i.x/2)] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                                    else:
                                        if coordinates[i.y-2][ceil(i.x/2)] == "Black" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x+1:
                                                    kill_checker = k
                                        if coordinates[i.y-2][ceil(i.x/2)-1] == "Black" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(bc)):
                                                if bc[k].y == i.y-1 and bc[k].x == i.x-1:
                                                    kill_checker = k
                                        

                        else:
                            '''e = 0
                            x = i.x
                            y = i.y
                            while e == 0:
                                x += 1
                                y += 1
                                if coordinates[i.y-1][int(i.x/2)-1]'''
                                
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
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and coordinates[i.y-3][ceil(i.x/2)] == "Nothnig":
                                        coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                kill_checker = k
                                elif i.x == 7:
                                    if coordinates[i.y-2][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-2] == "White" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y-2][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-2] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-2] == "White" and coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)-2] = 'Kill_step'
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-3][ceil(i.x/2)] = 'Kill_step'
                                        for k in range(len(wc)):
                                            if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                kill_checker = k
                            else:
                                checker = j
                                if i.x == 8:
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                    kill_checker = k
                                elif i.x == 2:
                                    if coordinates[i.y-2][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                    kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                else:
                                    if coordinates[i.y-2][ceil(i.x/2)-1] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)-1] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)-1] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x-1:
                                                    kill_checker = k
                                    if coordinates[i.y-2][ceil(i.x/2)] == "Nothing":
                                        coordinates[i.y-2][ceil(i.x/2)] = "Step"
                                    elif coordinates[i.y-2][ceil(i.x/2)] == "White" and i.y != 2:
                                        if coordinates[i.y-3][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y-3][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y-1 and wc[k].x == i.x+1:
                                                    kill_checker = k
                            if i.y != 7 and i.y != 8:
                                checker = j
                                if i.y % 2 == 1:
                                    if i.x == 1:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    kill_checker = k
                                    if i.x == 7:
                                        if coordinates[i.y][ceil(i.x/2)-2] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = 'Kill_step'
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    kill_checker = k
                                    else:
                                        if coordinates[i.y][ceil(i.x/2)-2] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == "Nothing":
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    kill_checker = k
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'While' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    kill_checker = k
                                else:
                                    if i.x == 8:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(wc)):
                                                    if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                        kill_checker = k
                                    elif i.x == 2:
                                        if coordinates[i.y][ceil(i.x/2)] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = 'Kill_step'
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    kill_checker = k
                                    else:
                                        if coordinates[i.y][ceil(i.x/2)-1] == 'White' and coordinates[i.y+1][ceil(i.x/2)-2] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)-2] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x-1:
                                                    kill_checker = k
                                        if coordinates[i.y][ceil(i.x/2)] == 'White' and coordinates[i.y+1][ceil(i.x/2)] == 'Nothing':
                                            coordinates[i.y+1][ceil(i.x/2)] = "Kill_step"
                                            for k in range(len(wc)):
                                                if wc[k].y == i.y+1 and wc[k].x == i.x+1:
                                                    kill_checker = k



                        else:
                            pass
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
                        if i.y == 8:
                            i.queen = 1
                        print(coordinates)
                        break
                    else:
                        step = 'White'
                        coordinates[bc[checker].y-1][ceil(bc[checker].x/2)-1] = 'Nothing'
                        bc[checker].move(i.x,i.y)
                        bc[checker].y = i.y
                        bc[checker].x = i.x
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'Black'
                        print(coordinates)
                        break
            for i in kill_steps:
                pos = mouse.get_pos()
                if i.rect.collidepoint(pos):
                    if step == "White":
                        step = 'Black'
                        coordinates[wc[checker].y-1][ceil(wc[checker].x/2)-1] = 'Nothing'
                        wc[checker].move(i.x,i.y)
                        wc[checker].y = i.y
                        wc[checker].x = i.x
                        coordinates[bc[kill_checker].y-1][ceil(bc[kill_checker].x/2)-1] = "Nothing"
                        del bc[kill_checker]
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'White'
                        print(coordinates)
                        break
                    else:
                        step = 'White'
                        coordinates[bc[checker].y-1][ceil(bc[checker].x/2)-1] = 'Nothing'
                        bc[checker].move(i.x,i.y)
                        bc[checker].y = i.y
                        bc[checker].x = i.x
                        coordinates[wc[kill_checker].y-1][ceil(wc[kill_checker].x/2)-1] = "Nothing"
                        del wc[kill_checker]
                        coordinates[i.y-1][ceil(i.x/2)-1] = 'Black'
                        print(coordinates)
                        break
                    

        

        
        if e.type == QUIT:
            game = False

    if coordinates2 != coordinates:
        print(coordinates)

    clock.tick(60)
    display.update()
