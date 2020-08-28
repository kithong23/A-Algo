import sys, pygame, math
pygame.init()

#modify here
sizex = 60
sizey = 60
squaresize = 13
startposition = 1, 1 #(y,x)
endposition = sizex - 2, sizey - 2 #(y,x)

#dont modify here (graphics setup)

black = 0, 0, 0
size = width, height = sizex * squaresize, sizey * squaresize
clickx = -10
clicky = -10
steps = 0
ispressed = False
isunpressed = False

setup = True

#data
class spots:
    def __init__(self,x,y):
        self.i = x
        self.j = y
        self.total = 0
        self.travelled = 0
        self.togo = 0
        self.value = 1
        self.neighbour = []
        self.previous = []
        self.obstacle = False
        self.checked = False
        self.start = False
        self.end = False
        self.finalpath = False

    def neighbors(self, box):

        if (self.i - 1) > -1 and box[self.j][self.i - 1].obstacle == False and box[self.j][self.i - 1].checked == False:
            self.neighbour.append(box[self.j][self.i - 1])
        if (self.j - 1) > -1 and box[self.j - 1][self.i].obstacle == False and box[self.j - 1][self.i].checked == False:
            self.neighbour.append(box[self.j - 1][self.i])
        if (self.i + 1) < sizex and box[self.j][self.i + 1].obstacle == False and box[self.j][self.i + 1].checked == False:
            self.neighbour.append(box[self.j][self.i + 1])
        if (self.j + 1) < sizey and box[self.j + 1][self.i].obstacle == False and box[self.j + 1][self.i].checked == False:
            self.neighbour.append(box[self.j + 1][self.i])

        for x in range(len(self.neighbour)):
            temptravelled = self.travelled + self.value
            if self.neighbour[x] not in openset:
                temptravelled = self.travelled + self.value
                self.neighbour[x].travelled = temptravelled
                self.neighbour[x].previous = self
                openset.append(self.neighbour[x])
            else:
                if temptravelled < self.neighbour[x].travelled:
                    self.neighbour[x].travelled = temptravelled

box = [[0] * sizex for i in range(sizey)]
for y in range(sizey):
    for x in range(sizex):
        box[y][x] = spots(x, y)

box[startposition[0]][startposition[1]].start = True
box[endposition[0]][endposition[1]].end = True
currentposition = box[startposition[0]][startposition[1]]
endposition = box[endposition[0]][endposition[1]]
reverse = endposition
openset = [box[startposition[0]][startposition[1]]]
closedset = []

def distancetoend(currentposition, endposition):
    distance = pow(pow((endposition.i - currentposition.i), 2) + pow((endposition.j - currentposition.j), 2), 0.5)
    return  distance

def findsmallest():
    smallestindex = 0
    for i in range(len(openset)):
        if openset[smallestindex].total > openset[i].total:
            smallestindex = i
    return smallestindex

#initialize
screen = pygame.display.set_mode(size)
screen.fill(black)
pygame.display.set_caption('AStar Algorithm')

while 1:
    screen.fill(black)

    while setup:
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    ispressed = True
                    clickx = math.ceil(mousepos[0] / squaresize) - 1
                    clicky = math.ceil(mousepos[1] / squaresize) - 1

                    box[clicky][clickx].obstacle = True
                elif event.button == 3:
                    isunpressed = True
                    clickx = math.ceil(mousepos[0] / squaresize) - 1
                    clicky = math.ceil(mousepos[1] / squaresize) - 1

                    box[clicky][clickx].obstacle = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ispressed = False
                elif event.button == 3:
                    isunpressed = False

            elif event.type == pygame.MOUSEMOTION:
                if ispressed == True:
                    clickx = math.ceil(mousepos[0] / squaresize) - 1
                    clicky = math.ceil(mousepos[1] / squaresize) - 1
                    box[clicky][clickx].obstacle = True
                elif isunpressed == True:
                    clickx = math.ceil(mousepos[0] / squaresize) - 1
                    clicky = math.ceil(mousepos[1] / squaresize) - 1
                    box[clicky][clickx].obstacle = False

            for y in range(sizey):
                for x in range(sizex):
                    if box[y][x].start == True:
                        pygame.draw.rect(screen, (100, 250, 50),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].end == True:
                        pygame.draw.rect(screen, (0, 0, 100),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].obstacle == True:
                        pygame.draw.rect(screen, (0, 100, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].obstacle == False:
                        pygame.draw.rect(screen, (100, 0, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
            pygame.display.update()
            if event.type == pygame.KEYDOWN:
                setup = False

    #Pathfinding
    if currentposition == endposition or len(openset) == 0:
        box[startposition[0]][startposition[1]].finalpath = True
        if reverse != box[startposition[0]][startposition[1]]:
            reverse.finalpath = True
            reverse = reverse.previous
            steps += 1
            for y in range(sizey):
                for x in range(sizex):
                    if box[y][x].start == True:
                        pygame.draw.rect(screen, (100, 250, 50),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].end == True:
                        pygame.draw.rect(screen, (0, 0, 100),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].obstacle == True:
                        pygame.draw.rect(screen, (0, 100, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    elif box[y][x].obstacle == False:
                        pygame.draw.rect(screen, (100, 0, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    if box[y][x].checked == True:
                        pygame.draw.rect(screen, (250, 0, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
                    if box[y][x].finalpath == True:
                        pygame.draw.rect(screen, (0, 250, 0),
                                         ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2),
                                         0)
            for i in range(len(openset)):
                pygame.draw.rect(screen, (100, 50, 250), (
                (openset[i].i * squaresize) + 1, (openset[i].j * squaresize) + 1, squaresize - 2, squaresize - 2), 0)

            pygame.display.update()

        elif reverse == box[startposition[0]][startposition[1]]:
            print('done')
            print(steps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            if event.type == pygame.KEYDOWN:
                openset.clear()
                openset = [box[startposition[0]][startposition[1]]]
                closedset.clear()

                for y in range(sizey):
                    for x in range(sizex):
                        box[y][x].checked = False
                        box[y][x].finalpath = False
                        box[y][x].neighbour.clear()
                currentposition = box[startposition[0]][startposition[1]]
                reverse = endposition
                steps = 0
                setup = True

    else:
        for x in range(len(openset)):
            openset[x].togo = distancetoend(openset[x], endposition)
            openset[x].total = openset[x].travelled + openset[x].togo

        smallestindex = findsmallest()
        currentposition = openset[smallestindex]

        closedset.append(currentposition)
        currentposition.checked = True

        if currentposition != endposition and len(openset) > 0:
            currentposition.neighbors(box)

        openset.pop(smallestindex)

        for y in range(sizey):
            for x in range(sizex):
                if box[y][x].start == True:
                    pygame.draw.rect(screen, (100, 250, 50), ((x * squaresize) + 1 , (y * squaresize) + 1, squaresize - 2, squaresize - 2), 0)
                elif box[y][x].end == True:
                    pygame.draw.rect(screen, (0, 0, 100), ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2), 0)
                elif box[y][x].obstacle == True:
                    pygame.draw.rect(screen, (0, 100, 0), ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2), 0)
                elif box[y][x].obstacle == False:
                    pygame.draw.rect(screen, (100, 0, 0), ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2), 0)
                if box[y][x].checked == True:
                    pygame.draw.rect(screen, (250, 0, 0), ((x * squaresize) + 1, (y * squaresize) + 1, squaresize - 2, squaresize - 2), 0)

        for i in range(len(openset)):
            pygame.draw.rect(screen, (100, 50, 250), ((openset[i].i * squaresize) + 1, (openset[i].j * squaresize) + 1, squaresize - 2, squaresize - 2), 0)

        pygame.draw.rect(screen, (250, 250, 250), ((currentposition.i * squaresize) + 1, (currentposition.j * squaresize) + 1, squaresize - 2, squaresize - 2), 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                openset.clear()
                openset = [box[startposition[0]][startposition[1]]]
                closedset.clear()
                currentposition = box[startposition[0]][startposition[1]]
                reverse = endposition
                for y in range(sizey):
                    for x in range(sizex):
                        box[y][x].checked = False
                        box[y][x].finalpath = False
                        box[y][x].neighbour.clear()
                setup = True

        pygame.display.update()
