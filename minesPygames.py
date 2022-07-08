import pygame
from random import randrange
from datetime import datetime

# initializing the constructor
pygame.init()
# set the pygame window name
pygame.display.set_caption('MineSweeper')
# screen resolution
res = (640, 672)
# square resolution
squareRes = (16, 16)
# field size
fieldSize = (int(res[0] / squareRes[0]), int(res[1] / squareRes[1]))

# opens up a window
screen = pygame.display.set_mode(res)

# mine dictionary, information about all squares
mineDic = {}

# get font
myFont = pygame.font.SysFont("Comic Sans MS", 20)

# colors
color_inside = (200, 200, 200)
color_border = (150, 150, 150)
color_white = (255, 255, 255)
color_light = (170, 170, 170)
color_darkGray = (100, 100, 100)
color_blue = (50, 150, 250)
color_orange = (250, 150, 50)

# importing images
emptyBtn = pygame.image.load(r"pics\emptyButton.png")
defaultBtn = pygame.image.load(r"pics\defaultButton.png")
oneBtn = pygame.image.load(r"pics\oneButton.png")
twoBtn = pygame.image.load(r"pics\twoButton.png")
threeBtn = pygame.image.load(r"pics\threeButton.png")
fourBtn = pygame.image.load(r"pics\fourButton.png")
fiveBtn = pygame.image.load(r"pics\fiveButton.png")
sixBtn = pygame.image.load(r"pics\sixButton.png")
sevenBtn = pygame.image.load(r"pics\sevenButton.png")
eightBtn = pygame.image.load(r"pics\eightButton.png")
expBombBtn = pygame.image.load(r"pics\expMine.png")
unExpBombBtn = pygame.image.load(r"pics\unexpMine.png")
flagBtn = pygame.image.load(r"pics\flag.png")

# game deactivation bool
gameActiveBool = True


# getting information about neighbors
def around(row, col):
    rowMax = fieldSize[0] - 1
    rowMin = 0
    colMax = fieldSize[1] - 1
    colMin = 2

    if row == rowMin or col == colMin:
        topLeft = None
    else:
        topLeft = [row - 1, col - 1]

    if col == colMin:
        left = None
    else:
        left = [row, col - 1]

    if row == rowMax or col == colMin:
        botLeft = None
    else:
        botLeft = [row + 1, col - 1]

    if row == rowMin or col == colMax:
        topRight = None

    else:
        topRight = [row - 1, col + 1]

    if col == colMax:
        right = None
    else:
        right = [row, col + 1]

    if row == rowMax or col == colMax:
        botRight = None
    else:
        botRight = [row + 1, col + 1]

    if row == rowMin:
        top = None
    else:
        top = [row - 1, col]

    if row == rowMax:
        bot = None
    else:
        bot = [row + 1, col]

    return topLeft, left, botLeft, topRight, right, botRight, bot, top


def initGen():
    # temporary values
    position = 0
    usedNums = []
    mines = 200

    global mineDic
    mineDic = {}

    # generating empty field
    for row in range(fieldSize[0]):
        for col in range(fieldSize[0]):
            mineDic[col * squareRes[0], (row * squareRes[1]) + 32] = {"status": 0, "position": position,
                                                                      "revealed": False, "flagged": False}
            position += 1

    # setting mines
    while mines > 0:
        randNum = randrange(fieldSize[0] * fieldSize[1])

        # checking if spot has been used to place a mine
        while randNum in usedNums:
            randNum = randrange(fieldSize[0] * fieldSize[1])

        for key, value in mineDic.items():
            if value["position"] == randNum:
                mineDic[key]["status"] = "X"
                mines -= 1

        usedNums.append(randNum)

    # setting values to non mines
    for spot, value in mineDic.items():
        if value["status"] != "X":
            tempCount = 0
            for cords in around(spot[0] / squareRes[0], spot[1] / squareRes[1]):
                if cords is not None:
                    if mineDic[int(cords[0] * squareRes[0]), int(cords[1] * squareRes[1])]["status"] == "X":
                        tempCount += 1

            value["status"] = tempCount

    # initial print of spots
    for key, value in mineDic.items():
        screen.blit(fillImage(value), key)


def fillImage(spotVars):
    numImages = (emptyBtn, oneBtn, twoBtn, threeBtn, fourBtn, fiveBtn, sixBtn, sevenBtn, eightBtn)

    if spotVars["revealed"]:
        if spotVars["status"] == "X":
            return unExpBombBtn

        else:
            return numImages[spotVars["status"]]
    else:
        return defaultBtn


def zeroReveal(spot):
    mineDic[spot]["revealed"] = True
    screen.blit(emptyBtn, spot)

    for cords in around(spot[0] / squareRes[0], spot[1] / squareRes[1]):
        if cords is not None:
            relativeCords = int(cords[0] * squareRes[0]), int(cords[1] * squareRes[1])

            if mineDic[relativeCords]["status"] == 0 and not mineDic[relativeCords]["revealed"]:
                mineDic[relativeCords]["revealed"] = True
                screen.blit(emptyBtn, relativeCords)
                zeroReveal(relativeCords)

            elif not mineDic[relativeCords]["revealed"]:
                mineDic[relativeCords]["revealed"] = True
                screen.blit(fillImage(mineDic[relativeCords]), relativeCords)


# generating a field before starting the game
initGen()

# getting time stuff
start_bool = False

global last_time
global start_time
global printTime


def timeTracked():
    global last_time
    global start_time
    global printTime
    global start_bool

    now = datetime.now()
    start_time = now.strftime("%H:%M:%S")
    last_time = start_time
    printTime = myFont.render("0", False, (250, 150, 50))

    start_bool = True


while gameActiveBool:

    # stores mouse coordinates into a tuple
    mouse = pygame.mouse.get_pos()
    relativeMouse = ((mouse[0] // 16) * 16, (mouse[1] // 16) * 16)

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            gameActiveBool = False
            # pygame.quit()

        # checking for mouse press
        elif ev.type == pygame.MOUSEBUTTONDOWN:

            timeTracked()
            # 1 for left click
            if ev.button == 1:
                # flag check
                if not mineDic[relativeMouse]["flagged"] or not mineDic[relativeMouse]["revealed"]:
                    #  bomb check
                    if mineDic[relativeMouse]["status"] == "X":
                        # display all bomb, reset button?
                        screen.blit(expBombBtn, relativeMouse)
                    # multi reveal if its a zero
                    elif mineDic[relativeMouse]["status"] == 0:
                        zeroReveal(relativeMouse)
                    # reveal anything not accounted for above
                    else:
                        mineDic[relativeMouse]["revealed"] = True
                        screen.blit(fillImage(mineDic[relativeMouse]), relativeMouse)
            # 2 for game reset (temporary)
            elif ev.button == 2:
                initGen()
            # 3 for right click
            elif ev.button == 3:
                if not mineDic[relativeMouse]["revealed"]:
                    if mineDic[relativeMouse]["flagged"]:
                        mineDic[relativeMouse]["flagged"] = False
                        screen.blit(fillImage(mineDic[relativeMouse]), relativeMouse)
                    else:
                        mineDic[relativeMouse]["flagged"] = True
                        screen.blit(flagBtn, relativeMouse)
    # box drawing, temporary?
    rowMax = 31
    colMax = 639
    pygame.draw.rect(screen, color_inside, [2, 2, 636, 28])
    for row in range(rowMax + 1):
        for col in range(colMax + 1):
            if row in [0, 1, rowMax - 1, rowMax]:
                pygame.draw.rect(screen, color_border, [col, row, 1, 1])
            if col in [0, 1, colMax - 1, colMax]:
                pygame.draw.rect(screen, color_border, [col, row, 1, 1])

        # drawing secs
    if start_bool:
        new = datetime.now()
        new_time = new.strftime("%H:%M:%S")

        if new_time != last_time:
            sec = int(new_time[6:8]) - int(start_time[6:8]) + (int(new_time[3:5]) - int(start_time[3:5])) * 60
            printTime = myFont.render(str(sec), False, (250, 150, 50))
            last_time = new_time
        screen.blit(printTime, (320, 0))

    # updates the frames of the game
    pygame.display.update()

"""
def timer():
    start = time.time()
    timing = 0
    while timing < 61:
        now = time.time()
        if timing != round(now-start):
            timing = round(now-start)
            print(timing)
"""

"""unused stuff from the initial, might be useful later
# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallFont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallFont.render('quit', True, color)

# fills the screen with a color
screen.fill((60, 25, 60))
    
    # if mouse is hovered on a button it
    # changes to lighter shade
    if width / 2 - 70 <= mouse[0] <= width / 2 - 70 + 140 and height / 2 - 20 <= mouse[1] <= height / 2 - 20 + 40:
        pygame.draw.rect(screen, color_light, [width / 2 - 70, height / 2 - 20, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width / 2 - 70, height / 2 - 20, 140, 40])
        
    # superimposing the text onto our button
    screen.blit(text, (width / 2 - 20, height / 2 - 20))
    
            # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, color_light, [(mouse[0] // 16) * 16, (mouse[1] // 16) * 16, 16, 16])
            # if the mouse is clicked on the
            # button the game is terminated
            
            if width / 2 - 70 <= mouse[0] <= width / 2 - 70 + 140 \
                    and height / 2 - 20 <= mouse[1] <= height / 2 - 20 + 40:
                gameActiveBool = False
                # pygame.quit()
"""

""" testing field generation
for key,value in mineDic.items():
  if value["status"] =="X":
    print(key,value)

print(len([key for key,value in mineDic.items() if value["status"] == "X"]))
print(len(mineDic))

for key,value in mineDic.items():
  if key[1] ==0:
    print(key,value)
"""
