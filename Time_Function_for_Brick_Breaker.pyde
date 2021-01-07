# VARIABLE MAP
# NAME               PURPOSE                                                                           TYPE                     LIMITATIONS
# boundary           0 = left boundary, 1 = right boundary,  2 = up boundary                           List
# imageList          List of images used in program                                                    List
# font               Font used to print ingame text                                                    Font                     
# gameScreen         Value for each gameScreen, 0 = menu, 1 = play, 2 = Help                           Integer                  0-2
# menuBar            List of clickboundaries in menuBar                                                List                          
# ball               x and y coordinate, width, height, x and y increment, colour, active/not active   List
# paddle             x and y coordinate, width, height, curve, paddle powerup time                                          List
# powerUp            x and y coordinate, width, height, curve                                          List
# time               active, elapsed time, remaining time                                              List
# name               name, character limit                                                             List
# abc                list of valid letters                                                             List
# numBrick           number of bricks in the game                                                      Integer                  100
# brickX             X coordinate for set of bricks                                                    Integer                  0
# brickY             Y coordinate for set of bricks                                                    Integer                  100
# brickInfo          List of info about each brick                                                     List
# allBrickInfo       List of all the bricks in the game                                                List

import random

def setup():
    global boundary, imageList, font
    global gameScreen, menuBar, ball, paddle, powerUp, time
    global numBrick, brickX, brickY, brickInfo, allBrickInfo
    
    size(601, 701)
    boundary = [0, 600, 0]
    imageList = [loadImage("menubar.png"), loadImage("title.png"), loadImage("space.jpg"), loadImage("help.png"), loadImage("black.jpg")]
    font = loadFont("OCRAExtended-48.vlw")
    gameScreen = 0
    menuBar = [[30, 620, 190, 680], [220, 620, 380, 680], [410, 620, 570, 680]]
    ball = [300, 515, 20, 20, 0, 0, 0, 5, False]
    ellipseMode(CENTER)
    paddle = [260, 535, 80, 15, 255, 0]
    powerUp = [random.randint(50,600), 20, 40, 10, 255]
    time = [False, 0, 30]
    numBrick = 100
    brickX = 0
    brickY = 100
    brickInfo = [0, 0, 0, 0, 0]
    allBrickInfo = [brickInfo [:] for i in range (numBrick)]
    for i in range(10):
        for j in range(10):
            allBrickInfo[10*i+j][0] = brickX#x
            allBrickInfo[10*i+j][1] = brickY#y
            allBrickInfo[10*i+j][2] = 60 #width
            allBrickInfo[10*i+j][3] = 15 #height
            allBrickInfo[10*i+j][4] = 0 #hitcounter
            brickX += 60
        brickY += 15
        brickX = 0
    
    add_library('minim')
    minim = Minim(this)
    sound = minim.loadFile("music.mp3")
    sound.loop()

def keyPressed():
    if gameScreen == 1:
        if ball[7] != 0:
            if key == "a" and paddle[0] > boundary[0]:
                if not(ball[8]):    
                    if ball[4] == 0 and ball[5] == 0:
                        ball[4] = -1
                        ball[5] = -5
                    time[0] = True
                    ball[8] = True
                paddle[0] -= 25
            if key == "d" and paddle[0] < boundary[1] - paddle[2]:
                if not(ball[8]):
                    if ball[4] == 0 and ball[5] == 0:
                        ball[4] = 1
                        ball[5] = -5
                    time[0] = True
                    ball[8] = True
                paddle[0] += 25

    
def mouseReleased():
    global boundary, imageList, font
    global gameScreen, menuBar, ball, paddle, time
    global numBrick, brickX, brickY, brickInfo, allBrickInfo
    
    menuM = False
    menuMX = menuBar[0][0] <= mouseX <= menuBar[0][2]
    menuMY = menuBar[0][1] <= mouseY <= menuBar[0][3]
    menuM = menuMX and menuMY
    if menuM:
        gameScreen = 0
        time[0] = False
        ball[8] = False
    
    menuP = False
    menuPX = menuBar[1][0] <= mouseX <= menuBar[1][1]
    menuPY = menuBar[1][2] <= mouseY <= menuBar[1][3]
    menuP = menuPX and menuPY
    if menuP:
        gameScreen = 1
        
    if gameScreen == 1:
        if ball[7] == 0:
            replayX = 240 <= mouseX <= 360
            replayY = 330 <= mouseY <= 350
            replayPlay = replayX and replayY
            if replayPlay:
                for i in range(10):
                    for j in range(10):
                        allBrickInfo[10*i+j][4] = 0
                ball = [300, 515, 20, 20, 0, 0, 0, 5, False]
                time = [False, 0, 30]
            

    
    menuH = False
    menuHX = menuBar[2][0] <= mouseX <= menuBar[2][1]
    menuHY = menuBar[2][2] <= mouseY <= menuBar[2][3]
    menuH = menuHX and menuHY
    if menuH:
        gameScreen = 2
        time[0] = False
        ball[8] = False
    
    
def checkBrickHit(ball, allBrickInfo):
    if allBrickInfo[4] < 3:
        if ball[0] <= allBrickInfo[0] + allBrickInfo[2] + ball[2]/2 and ball[1] >= allBrickInfo[1] and ball[1] <= allBrickInfo[1] + allBrickInfo[3] and ball[0] > allBrickInfo[0] + allBrickInfo[2]/2:
            if ball[4] < 0:
                ball[4] = - ball[4]
                allBrickInfo[4] += 1
                ball[6] += 100
        if ball[0] >= allBrickInfo[0] - ball[2]/2 and ball[1] >= allBrickInfo[1] and ball[1] <= allBrickInfo[1] + allBrickInfo[3] and ball[0] < allBrickInfo[0] + allBrickInfo[2]/2:
            if ball[4] > 0:
                ball[4] = - ball[4]
                allBrickInfo[4] += 1
                ball[6] += 100
        if ball[1] <= allBrickInfo[1] + allBrickInfo[3] + ball[3]/2 and ball[0] >= allBrickInfo[0] and ball[0] <= allBrickInfo[0] + allBrickInfo[2] and ball[1] > allBrickInfo[1] + allBrickInfo[3]/2:
            if ball[5] < 0:
                ball[5] = -ball[5]
                allBrickInfo[4] += 1
                ball[6] += 100
        if ball[1] >= allBrickInfo[1] - ball[3]/2 and ball[0] >= allBrickInfo[0] and ball[0] <= allBrickInfo[0] + allBrickInfo[2] and ball[1] < allBrickInfo[1] + allBrickInfo[3]/2:
            if ball[5] > 0:
                ball[5] = -ball[5]
                allBrickInfo[4] += 1
                ball[6] += 100
    return(ball, allBrickInfo[4])
    
def draw():
    global boundary, imageList, font
    global gameScreen, menuBar, ball, paddle, powerUp, time
    global numBrick, brickX, brickY, brickInfo, allBrickInfo
    global shrinkPaddle
    
    if gameScreen == 0:
        image(imageList[1], 0, 0)
    
    if gameScreen == 1:
        image(imageList[2], 0, 0)
    
        textAlign(CENTER)
        textFont(font, 30)
        text("SCORE:", 60, 40)
        text(ball[6], 157, 40)
    
        text("POWERUP:", 400, 40)
        text(time[2], 500, 40)

        for i in range(ball[7]-1):
            ellipse(15 + i*30 , 575, 20, 20)
        
        for i in range(10):
            for j in range(10):
                if allBrickInfo[10*i+j][4] == 0:
                    fill(144, 238, 144)
                if allBrickInfo[10*i+j][4] == 1:
                    fill(255, 215, 0)
                if allBrickInfo[10*i+j][4] == 2:
                    fill(255, 0, 0)
                if allBrickInfo[10*i+j][4] < 3:
                    rect(allBrickInfo[10*i+j][0], allBrickInfo[10*i+j][1], allBrickInfo[10*i+j][2], allBrickInfo[10*i+j][3])
        
        if time[0]:
            s = second()
            if time[1] != s and time[2] > 0:
                time[2] -= 1
                time[1] = s
            if time[2] == 0:
                fill(85,51,255)
                rect(powerUp[0], powerUp[1], powerUp[2], powerUp[3], powerUp[4])
                powerUp[1] += 2
            
            if paddle[2] == 120 and time[1] >= paddle[5]:
                paddle[2] = 80
        
        
        
        fill(0)
        rect(paddle[0], paddle[1], paddle[2], paddle[3], paddle[4])
        
        fill(255)
        ellipse(ball[0], ball[1], ball[2], ball[3])
        if ball[8]:
            ball[0] += ball[4]
            ball[1] += ball[5]
        
        if ball[0] <= boundary[0] + ball[2]/2 or ball[0] >= boundary[1] - ball[2]/2:
            ball[4] = -ball[4]
            
        if ball[1] <= boundary[2] + ball[3]/2:
            ball[5] = -ball[5]
        
        if ball[1] > paddle[1] + 50:
            ball = [300, 515, 20, 20, 0, 0, ball[6], ball[7], ball[8]]
            paddle = [260, 535, 80, 15, 255]
            time[0] = False
            ball[7] -= 1
            ball[8] = False

        
        if ball[0] < paddle[0] + paddle[2]/2 and ball[0] > paddle[0] and ball[1] > paddle[1] - ball[3]/2 and ball[1] < paddle [1] - ball[3]/2 + 10:
            ball[4] = -2
            ball[5] = -ball[5]
        
        if ball[0] < paddle[0] + paddle[2] and ball[0] > paddle[0] + paddle[2]/2 and ball[1] > paddle[1] - ball[3]/2 and ball[1] < paddle [1] - ball[3]/2 + 10:
            ball[4] = 2
            ball[5] = -ball[5]
            
        if (powerUp[1] > paddle[1]):
            if (powerUp[0] < (paddle[0] + paddle[2]) and (powerUp[0] + paddle[2]) > paddle[0]):
                paddle[2] = 120
                paddle[5] = time[1] + 10
                fill (0)
                rect(paddle[0], paddle[1], paddle[2], paddle[3], paddle[4])
            else:
                paddle[2] = 80
            powerUp[0] = random.randint(50,600)
            powerUp[1] = 0
            time[2] = 30
            time[1] = s
            
        for i in range(10):
            for j in range(10):
                if ball[1] > 90 and ball[1] < 260:
                    ball, allBrickInfo[10*i+j][4] = checkBrickHit(ball, allBrickInfo[10*i+j])
        
        if ball[7] == 0:
            tint(0, 200)
            image(imageList[4], 0, 0)
            text("REPLAY?", 300, 350)           
            textFont(font, 60)
            text("SCORE:", 200, 300)
            text(ball[6], 395, 300)
        tint(255)
    
    if gameScreen == 2:
        image(imageList[3],0, 0)
    
    image(imageList[0], 0, 600)
    
    #print(mouseX, mouseY)