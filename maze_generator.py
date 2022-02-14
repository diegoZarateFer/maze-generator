#Diego Zárate Fernández
#Date: 21/04/2020
#Mazes generator

import pygame as pg
import random

#Initialize pygame
pg.init()

#Settings
WIDTH,HEIGHT = 600,600
FPS = 60

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (255,0,255)
BLUE = (0,0,255,100)

w = 20
cols = WIDTH//w
rows = HEIGHT//w
grid = []
stack = []

class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True,True,True,True]

    def check_neighbors(self,grid):
        neighbors = []

        if self.y+1 < rows and not grid[self.x][self.y+1].visited:
            neighbors.append(grid[self.x][self.y+1])
        if self.y-1 >= 0 and not grid[self.x][self.y-1].visited:
            neighbors.append(grid[self.x][self.y-1])
        if self.x+1 < cols and not grid[self.x+1][self.y].visited:
            neighbors.append(grid[self.x+1][self.y])
        if self.x-1 >= 0 and not grid[self.x-1][self.y].visited:
            neighbors.append(grid[self.x-1][self.y])
        if len(neighbors) > 0:
            return random.choice(neighbors)
        return None

    def highlight(self,screen):
        pg.draw.rect(screen,PURPLE,(self.x*w,self.y*w,w,w),0)

    def draw(self,screen):
        x = self.x*w
        y = self.y*w

        if self.visited:
            pg.draw.rect(screen,WHITE,(x,y,w,w),0)

        #top
        if self.walls[0]:
            pg.draw.line(screen,BLACK,(x,y),(x+w,y),1)
        #right
        if self.walls[1]:
            pg.draw.line(screen,BLACK,(x+w,y+w),(x+w,y),1)
        #bottom
        if self.walls[2]:
            pg.draw.line(screen,BLACK,(x,y+w),(x+w,y+w),1)
        #left
        if self.walls[3]:
            pg.draw.line(screen,BLACK,(x,y),(x,y+w),1)

def remove_walls(a,b):
    x = a.x - b.x
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False

    y = a.y - b.y

    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False

#Initialize the screen
screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("MAZE GENERATOR")
screen.fill(BLUE)

#creating the grid
for row in range(rows):
    l = []
    for col in range(cols): l.append(Cell(row,col))
    grid.append(l)

current = grid[0][0]
current.visited = True

#Clock
clock = pg.time.Clock()

running = True
while running:

    #events
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

    next = current.check_neighbors(grid)
    if next != None:
        next.visited = True
        stack.append(current)
        remove_walls(current,next)
        current = next
    elif len(stack) > 0:
        current = stack.pop()

    #drawing
    for i in grid:
        for j in i: j.draw(screen)
    current.highlight(screen)

    clock.tick(FPS)
    pg.display.flip()

pg.quit()
