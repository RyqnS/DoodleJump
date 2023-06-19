# from cmu_112_graphics import *
from cmu_cs3_graphics import *
import random
import math

##
class Shuriken:
    def __init__(self,d,dis,x,y,r,width):
        self.x = x
        self.y = y
        self.r = r
        self.d = d
        self.dis = dis
        self.max = x + self.dis
        if x - self.dis < 0:
            self.min = 0
        else:
            self.min = x - self.dis
        if x + self.dis > width:
            self.max = width - r
        else:
            self.max = x + self.dis
    def move(self):
        self.x += self.d
        if (self.x+self.r > self.max):
            #self.x -= self.d
            self.x = self.r
    def draw(self,app,rA):
        drawStar(self.x,self.y,self.r,4,fill="black",rotateAngle = rA)

class Platform:
    def __init__(self,x,y,w,le):
        self.x = x
        self.y = y
        self.w = w
        self.le = le
    def draw(self,app):
        drawRect(self.x,self.y,self.w,self.le,fill="red")
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

class movingPlatform(Platform):
    def __init__(self,d,dis,x,y,w,le,width):
        super().__init__(x,y,w,le)
        self.d = d
        self.dis = dis
        self.max = x + self.dis
        if x - self.dis < 0:
            self.min = 0
        else:
            self.min = x - self.dis
        if x + self.dis > width:
            self.max = width - w
        else:
            self.max = x + self.dis

    def move(self):
        self.x += self.d
        if (self.x > self.max) or (self.x < -self.max) or (self.x < self.min):
            #self.x -= self.d
            self.d = -self.d
    def draw(self,app):
        drawRect(self.x,self.y,self.w,self.le,fill="green")


class fragilePlatform(Platform):
    def __init__(self, num, x, y, w, le):
        super().__init__(x,y,w,le)
        self.life = num
    def decrease(self):
        self.life -= 1
    def draw(self,app):
        drawRect(self.x,self.y,self.w,self.le,fill="blue")
##

def genNewPlat(app):
    lasty = app.platforms[-1].y
    num = random.randint(0, 31)
    if num in range(0, 15):
        genRandPlat(app,lasty)
    elif num in range(15, 26):
        genRandMovingPlat(app,lasty)
    else:
        genRandFragPlat(app,lasty)
    newnum = random.randint(0,10)
    if num <= app.numShurikens:
        genShuriken(app,lasty)

def genRandPlat(app,lasty):
    w = random.randint(50, app.width/4)
    le = app.platLen
    x = random.randint(0, app.width - w)
    y = random.randint(10, app.height//4) #change this back
    plat = Platform(x,lasty-y,w,le)
    app.platforms.append(plat)

def genRandMovingPlat(app,lasty):
    d = random.randint(2, (2 + (app.score//800)))
    dis = random.randint(5*d, 50000) 
    w = random.randint(50, app.width/4)
    le = app.platLen
    x = random.randint(0, app.width - w)
    y = random.randint(10,app.height//4) ##change this back
    plat = movingPlatform(d,dis,x,lasty-y,w,le,app.width)
    app.platforms.append(plat)

def genRandFragPlat(app,lasty):
    num = 1
    w = random.randint(50, app.width/4)
    le = app.platLen
    x = random.randint(0, app.width - w)
    y = random.randint(10, app.height//4) #change this back
    plat = fragilePlatform(num, x, lasty-y, w, le)
    app.platforms.append(plat)

def genShuriken(app,lasty):
    d = random.randint(2, (2 + (app.score//600)))
    dis = random.randint(5*d, 50000) 
    r = random.randint(10,app.platLen*2)
    x = random.randint(0, app.width - r)  
    star = Shuriken(d,dis,x,lasty-r,r,app.width)
    app.shurikens.append(star)

def onAppStart(app):
    loadGame(app)

def loadGame(app):
    app.timer = 0
    app.numShurikens = 0
    app.score = 0
    app.screencount = 1 
    app.radius = (app.width+app.height)//100
    app.cx = app.width//2
    app.cy = app.height- app.radius -16
    app.platformPaused = False
    app.platforms = []
    app.shurikens = []
    app.ay = 0.5  # pixels/(time of iteration)^2
    app.truevy = 0
    app.vy = app.truevy
    app.dx = 5+app.width//300
    app.vx = 0
    app.gameOver = False
    app.baseplat = Platform(0,app.height,app.width,10)
    app.platLen = app.width//100
    app.platforms.append(app.baseplat)
    generateStartingPlats(app)
    app.currentPlat = app.platforms[0]
    app.goingUp = True
    app.screenShift = False
    app.maxPlatforms = 20
    app.gameStarted = False
    app.gameMode = 0
    app.message = "Doodle Jump?"
    app.doubleJumps = 1
    app.djTimer = 0
    app.bounceMode = False
    app.slideMode = False
    initializeRandomBalls(app)

def initializeRandomBalls(app):
    app.randBallCounts = (app.width*app.height)//15000
    app.randBallRadius = 8
    app.randBalls = []
    for i in range(app.randBallCounts):
        bx = random.randint(app.randBallRadius, app.width-app.randBallRadius)
        by = random.randint(app.randBallRadius, app.height-app.randBallRadius)
        dx = random.randint(1, 5)
        dy = random.randint(1, 5)
        colorList = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        color = random.choice(colorList)
        app.randBalls.append((bx, by, dx, dy, color))

def generateStartingPlats(app): 
    while len(app.platforms)<12:
        lasty = app.platforms[-1].y
        genNewPlat(app)

def redrawAll(app): # Draws one of three screens
    if (app.screencount ==1):
        drawScreen1(app) 
    elif (app.screencount ==2):
        drawGame(app)
    elif(app.screencount ==3):
        drawLose(app)

def drawScreen1(app): # 1
    drawRect(app.width//2 - app.width//8, app.height - app.height//6, 
            app.width//4, app.height//8, fill = None, border = 'black', borderWidth = min(app.width,app.height)//100)
    drawLabel("Start",app.width//2 - app.width//6+ (app.width//3)//2, 
            app.height - app.height//6+ (app.height//8)//2, size = ((app.width//2 - app.width//6)+(app.height - app.height//4))//20 )
    drawLabel(f"{app.message}",app.width//2, .5*app.height//6,size = app.radius *3)
    
    drawCircle(app.width//2, 1.75*app.height//6,app.height//12, fill = 'green', border = 'black')
    drawCircle(app.width//2, 3* app.height//6,app.height//12, fill = 'yellow', border = 'black')
    drawCircle(app.width//2, 4.25* app.height//6,app.height//12, fill = 'red', border = 'black')
    for numlabel in range(len(["Easy","Medium","Hard"])):
        label = ["Easy","Medium","Hard"][numlabel]
        bolds = True if app.gameMode == numlabel+1 else False
        drawLabel(label,app.width//2,(0.5+((numlabel+1)*1.25))*app.height//6,size = app.radius *2,bold = bolds)
    drawRect(app.radius*10,app.radius*3,app.height//4,app.height//12, fill = 'pink', border = 'black', align='center')
    drawRect(app.width-app.radius*10,app.radius*3,app.height//4,app.height//12, fill = 'violet', border = 'black', align='center')
    drawLabel('BOUNCE',app.radius*10,app.radius*3,size = app.radius*2,bold = app.bounceMode)
    drawLabel('SLIDE',app.width-app.radius*10,app.radius*3,size = app.radius*2,bold = app.slideMode)
    drawRandomBalls(app)
        
def drawRandomBalls(app):
    for bx, by, _, _, color in app.randBalls:
        drawCircle(bx, by, app.randBallRadius, fill=color)

def drawGame(app): #2
    for platform in app.platforms:
        platform.draw(app)
    drawBall(app)
    drawLabel(f'Score: {int(app.score//10)}',app.width//2,app.height//15,size = app.radius*2)
    if app.doubleJumps == 1:
        drawLabel(f'Double Jumps: ACTIVE',app.width-app.width//8, app.height - app.height//15, size = app.radius )
    elif app.djTimer > 0:
        drawLabel(f'Double Jump In: {math.ceil(app.djTimer/30)}',app.width-app.width//8, app.height - app.height//15, size = app.radius )
    if not app.gameStarted:
        drawRect(app.width//9, app.height-app.height//3,app.width-(app.width//4.5),app.height//4,fill = 'lightgrey')
        drawLabel("Rules: Press 'space' to start, try to get the highest score!", app.width//2,app.height - app.height//4 + -0.25*app.height//10, size = app.radius*1.5)
        drawLabel("Red platforms are your friend", app.width//2,app.height - app.height//4 + 0.35*app.height//10, size = app.radius)
        drawLabel("Green platforms are on the move", app.width//2,app.height - app.height//4 + 0.7*app.height//10, size = app.radius)
        drawLabel("Blue platforms shatter after one bounces", app.width//2,app.height - app.height//4 + 1.05*app.height//10, size = app.radius)
        drawLabel("Don't touch the shurikens or fall from too high!",app.width//2,app.height - app.height//4 + 1.4*app.height//10, size = app.radius)
    
    for shuriken in app.shurikens:
        shuriken.draw(app,app.timer*20)
    
def drawBall(app): #1a
    drawCircle(app.cx,app.cy,app.radius, fill = None, border = 'black')
    if app.cx > app.width - app.radius:
        cx = app.cx - app.width
        drawCircle(cx, app.cy, app.radius, fill = None, border = 'black')

def drawLose(app): #3
    drawLabel("YOU DIED. Press R to Restart.",app.width//2,app.height//2,fill = 'red')

def onStep(app):
    takeStep(app)

def takeStep(app):
    app.timer+=1
    if app.djTimer == 0 and app.doubleJumps == 0:
        app.doubleJumps = 1
    elif app.djTimer > 0 and app.doubleJumps == 0:
        app.djTimer -= 1 
    ballMove(app)
    editPlatform(app)
    for platform in app.platforms:
        if type(platform) == movingPlatform:
            platform.move()
    for shuriken in app.shurikens:
        shuriken.move()
    moveRandBalls(app)

def editPlatform(app): # Moves platforms to create the illusion of following the ball
    if(app.cy<app.height//2 and app.goingUp == True):
        if len(app.platforms) < app.maxPlatforms:
            genNewPlat(app)
        app.screenShift = True
        for index in range(len(app.platforms)):
            platform = app.platforms[index]
            platform.y -= app.vy
            app.score += abs(app.vy)//10
        for shuriken in app.shurikens:
            shuriken.y -= app.vy
            
    else: 
        app.screenShift = False
        counter = 0
        while counter < len(app.platforms):
            platform = app.platforms[counter]
            if(platform.y > app.height):
                app.platforms.pop(counter) 
                print(len(app.platforms))
            else:
                counter+=1   

def ballMove(app): #bounces ball by default
    if not app.gameOver:
        if app.screenShift == False:
            app.cy += app.vy
        app.vy += app.ay
        if app.vy >=0:
            app.goingUp = False
        if app.bounceMode:
            checkBallHitPlatform(app)
        else:
            if ballHitPlatform(app) and app.goingUp == False:
                app.vy = app.truevy
                app.goingUp = True
        if app.slideMode:
            app.cx += app.vx
        if (app.cy > app.height or ballHitShuriken(app)) and (not app.screencount==1):
            app.screencount = 3
            app.gameOver = True

def ballHitShuriken(app):
    for index in range(len(app.shurikens)):
        shuriken = app.shurikens[index]
        left, top,r  = shuriken.x, shuriken.y, shuriken.r
        if dis(app.cx,app.cy,left,top) <=app.radius + r:
            return True
    return False

def ballHitPlatform(app): 
    for index in range(len(app.platforms)):
        platform = app.platforms[index]
        left, top = platform.x, platform.y
        width, length = platform.w, platform.le
        if left -app.radius//2 <= app.cx <= left + width+app.radius//2:
            if top <= app.cy+app.radius <= top+length+app.radius:
                if(app.goingUp == False):
                    app.cy= top - app.radius
                    if isinstance(platform, fragilePlatform):
                        platform.decrease()
                        print(platform.life)
                        if platform.life <= 0:
                            app.platforms.pop(index)
                app.currentPlat = app.platforms[index]
                return True
    return False

def checkBallHitPlatform(app): 
    if not app.gameOver:
        index = 0
        while index < len(app.platforms):
            platform = app.platforms[index]
            left, top = platform.x, platform.y
            width, length = platform.w, platform.le
            right, bottom = platform.x + platform.w, platform.y + platform.le
            closestX = max(left, min(app.cx, right))
            closestY = max(top, min(app.cy,bottom))
            if dis(app.cx, app.cy, closestX, closestY) <= app.radius:
                app.currentPlat = app.platforms[index]
                deltaY = app.cy - closestY
                deltaX = app.cx - closestX
                theta = math.atan2(deltaY, deltaX)
                if almostEqual(math.sin(theta), -1) :
                    app.vy = app.truevy
                    app.goingUp = True
                elif math.sin(theta) > 0:
                    app.vy *= -1
                if not almostEqual(math.cos(theta),0):
                    app.vx = math.cos(theta) * app.truevy * 0.3 
                app.cx = closestX + math.cos(theta) * app.radius
                app.cy = closestY + math.sin(theta) * app.radius
                if isinstance(platform, fragilePlatform):
                        platform.decrease()
                        print(platform.life)
                        if platform.life <= 0:
                            app.platforms.pop(index)
                else: index += 1
            else: index += 1

def moveRandBalls(app):
    if app.screencount == 1:
        for i in range(len(app.randBalls)):
            bx, by, dx, dy, color = app.randBalls[i]
            bx += dx
            radius = app.randBallRadius
            if bx >= app.width - radius:
                bx = app.width - radius  
                dx = -dx
            elif bx <= radius:
                bx = radius
                dx = -dx
            by += dy
            if by >= app.height - radius:
                by = app.height - radius  
                dy = -dy
            elif by <= radius:
                by = radius
                dy = -dy
            app.randBalls[i] = (bx, by, dx, dy, color)

def onKeyPress(app,key):
    if app.platformPaused and key == 's':
        takeStep(app)
    elif key =='p':
        app.paused = not app.paused
    elif key =='left': # moving character left
        app.cx -=5
    elif key =='right': # moving character right
        app.cx += 5
    elif key == 'r' and app.gameOver:
        loadGame(app)
    elif key == 'space': 
        if not app.gameStarted:
            app.truevy = -(app.height+(app.width*.25))//60
            app.gameStarted = True
        else:
            if app.doubleJumps == 1:
                app.vy = app.truevy
                app.goingUp = True
                editPlatform(app)
                app.doubleJumps = 0
                app.djTimer = 300



def onKeyHold(app,keys):
    if 'left' in keys: # moving character left
        if not app.slideMode:
            app.cx -= app.dx
        else:
            app.vx -= 0.2
        if app.cx - app.radius < 0:
            app.cx += app.width
       
    elif 'right' in keys: # moving character right
        if not app.slideMode:
            app.cx += app.dx
        else:
            app.vx += 0.2
        if app.cx >= app.width + app.radius:
            app.cx = app.radius

def onMousePress(app,mouseX,mouseY):
    topLeftX = app.width//2 - app.width//8
    topLeftY = app.height - app.height//6
    Xdim = app.width//4
    Ydim = app.height//8
    if app.screencount == 1:
        if(topLeftX <= mouseX<= topLeftX+Xdim) and (topLeftY<mouseY<topLeftY+Ydim):
            if app.gameMode > 0:
                app.screencount = 2
            else:
                app.message = 'Choose a difficulty!'

        if dis(app.width//2, 1.75*app.height//6,mouseX,mouseY) < app.height//12:
            app.gameMode = 1
            app.numShurikens = -1
        elif dis(app.width//2, 3*app.height//6,mouseX,mouseY) < app.height//12:
            app.gameMode = 2
            app.numShurikens = 1
        elif dis(app.width//2, 4.25*app.height//6,mouseX,mouseY) < app.height//12:
            app.gameMode = 3
            app.numShurikens = 5
        elif (app.radius*10 - app.height//8 <= mouseX <= app.radius*10 + app.height//8) and (app.radius*3-app.height//24 <= mouseY <= app.radius*3 + app.height//24):
            app.bounceMode = not app.bounceMode
        elif (app.width-app.radius*10-app.height//8 <= mouseX <= app.width-app.radius*10+app.height//8) and (app.radius*3-app.height//24 <= mouseY <= app.radius*3 + app.height//24):
            app.slideMode = not app.slideMode
    
def dis(x0,y0,x1,y1):
    return (((x0-x1)**2+(y0-y1)**2)**0.5)

def almostEqual(x, y):
    if abs(x-y) <= 10**(-5):
        return True
    return False

runApp(width=1512,height = 842)