import pygame, sys
import random
import datetime
import re
import time

pygame.init()

windowWidth = 300
windowHeight = 260
endscreen_color = (0, 0, 0)
scene = -1

win = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("RYBOLAND")


heart = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/heart.png')
shield = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/shield.png')
rybolbol = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/poke.png')
ryboldex = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/Ryboldex.png')
ball = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/ball.png')
E = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/E.png')
fullImg = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/fullScreen.png')
portal = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/portal.png')
timeBoard = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/timeBilboard.png')
mapBoard = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/GUI/map.png')
enemyImg = [pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/kaneki.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/rybol.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/rybolend.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/don.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/maksiq.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/kanekiend.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/donHit.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/mword.png')]
maksiqImg = [pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/maksiqHit1.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/maksiqHit2.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/maksiqHit3.png') ,pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Enemies/maksiqTeleport.png')]
bgZERO = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg-1.jpg')
bg = [pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg.jpg'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg2.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg3.png'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg2.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg5.jpg'),pygame.image.load('Rybols/Emulator_Tkinter/Sprites/Bg/bg4.png')]
npcImg = [pygame.image.load('Rybols/Emulator_Tkinter/Sprites/NPCs/mucher.png'), pygame.image.load('Rybols/Emulator_Tkinter/Sprites/NPCs/muchor.png')]


characterIdle = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/MC/character.png')
characterLeft = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/MC/characterLeft.png')
characterRight = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/MC/characterRight.png')
characterUp = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/MC/characterUp.png')
characterDown = pygame.image.load('Rybols/Emulator_Tkinter/Sprites/MC/characterDown.png')

drainggang = pygame.mixer.Sound('Rybols/Emulator_Tkinter/Sprites/SFx/draingang.wav')
drainggang.set_volume(0.5)
drainggang.play()

puff = pygame.mixer.Sound('Rybols/Emulator_Tkinter/Sprites/SFx/puff.wav')

sprint = pygame.mixer.Sound('Rybols/Emulator_Tkinter/Sprites/SFx/sprint.wav')

fresh = pygame.mixer.Sound('Rybols/Emulator_Tkinter/Sprites/SFx/fresh.wav')
fresh.set_volume(0.5)

music = pygame.mixer.music.load('Rybols/Emulator_Tkinter/Sprites/SFx/music.mp3')



pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


isFullscreen = False
fullClicked = False
winCon = False
shootBullet = False
canRight = True
canLeft = True
canDown = True
canUp = True
canShoot = True 

highlight = 0
isRecord = False
timeFin = 0
score = 0
dialogue = 0
clock = pygame.time.Clock()


class Player(object):
    def __init__(self, x, y, width, height):
        self.y = y 
        self.x = x
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.shoot = False
        self.isStanding = True
        self.hitbox = (self.x + 20, self.y, 24, 24)  
        self.isHit = False
        self.life = 5
        self.isShield = False
        ##Defines the hitbox it atributes will be refered as an list
        
    def draw(self, win): 
        global canRight, canLeft, canUp, canDown
        canRight = True
        canLeft = True
        canDown = True
        canUp = True
        if  self.left:
            win.blit(characterLeft, (self.x,self.y))
        elif self.right: 
            win.blit(characterRight, (self.x,self.y))
        elif self.down:
            win.blit(characterDown, (self.x,self.y))
        elif self.up: 
            win.blit(characterUp, (self.x,self.y))
            
        if self.isStanding:
            win.blit(characterIdle, (self.x,self.y))
        
        self.hitbox = (self.x, self.y, 24, 24) 
        self.check()
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)                        ##//SEE COLISION        

    def check(self):
        global canRight, canLeft, canUp, canDown, canShoot
        if self.isShield:
            win.blit(shield, (self.x, self.y))
            canRight = False
            canLeft = False
            canDown = False
            canUp = False
            canShoot = False
        if self.isHit == True and self.life > 0 and self.isShield == False:
            print("Attack")
            self.x = 100
            self.y = 20  
            self.life -= 1
            print(self.life)
            if self.life == 0:
                print("lose")
                self.die()
        self.isShield = False
        self.isHit = False
        canShoot = True

    def die(self):
        global scene
        scene = -2


class Enemy(object):
    def __init__(self, x, y, width, height, erange, etype, scene, shield):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.erange = erange
        self.pathx = [self.x, self.x+erange]
        self.pathy = [self.y, self.y+erange]
        self.stage = 0
        self.vel = 1    
        self.etype = etype                                                              ##Define type of enemy: SQ(square) or LR(left right)
        self.hitbox = (self.x + 20, self.y, self.width, self.height)      
        self.isRybolend = False 
        self.isDead = False  
        self.pokeView = False  
        self.scene = scene   
        self.shield = shield
                ##Define hitbox
        
    def draw(self, win):  
                                                                                            ##Type of enemy and adding asocieted photo
        if self.etype == "SQ":  
            win.blit(enemyImg[1], (self.x, self.y))    
            if self.pokeView == False:                                                  ##Type of enemy and asocieted pattern
                self.moveSq()
                
        elif self.etype == "SQr":  
                win.blit(enemyImg[2], (self.x, self.y))    
                if self.pokeView == False: 
                    self.vel = 10                                                 ##Type of enemy and asocieted pattern
                    self.moveSq()
            
        elif self.etype == "LR":
            win.blit(enemyImg[0], (self.x, self.y))
            if self.pokeView == False: 
                self.moveLR()
                
        elif self.etype == "LRDon":
            if self.shield == 1:
                win.blit(enemyImg[3], (self.x, self.y))
            elif self.shield == 0:
                win.blit(enemyImg[6], (self.x, self.y))
            if self.pokeView == False: 
                self.moveLR()
            else:
                win.blit(enemyImg[3], (self.x, self.y))
                
        elif self.etype == "Maksiq":
            
            if self.shield == 4:
                win.blit(enemyImg[4], (self.x, self.y))
            elif self.shield == 3:
                win.blit(maksiqImg[0], (self.x, self.y))
            elif self.shield == 2:
                win.blit(maksiqImg[1], (self.x, self.y))
            elif self.shield <= 1:
                win.blit(maksiqImg[2], (self.x, self.y))
                
            if self.pokeView == False: 
                self.moveMaq()
                
        elif self.etype == "LRr":
            win.blit(enemyImg[5], (self.x, self.y))
            if self.pokeView == False: 
                self.moveLRr()  

        elif self.etype == "Pix":
            win.blit(enemyImg[7], (self.x, self.y))
            if self.pokeView == False: 
                self.moveLRr()   
            
        self.hitbox = (self.x, self.y+5, self.width-5, self.height-10) 
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)   
        self.check(man)                              #//SEE COLISION

    def check(self, character):
        if character.x < self.x + self.width and character.x + character.width > self.x:
            if character.y < self.y + self.height and character.y  + character.height > self.y:
                character.isHit = True

    def moveLR(self):                                                            ##Loop for moving left and right
        if self.vel > 0:
            if self.x < self.pathx[1] + self.vel: 
                self.x += self.vel
            else: 
                self.vel = self.vel * -1
        else: 
            if self.x - self.vel > self.pathx[0]:
                self.x += self.vel
            else: 
                self.vel = self.vel * -1
                
    def moveLRr(self):                                                            ##Loop for moving left and right
        if self.vel > 0:
            if self.x < self.pathx[1] + self.vel: 
                self.x += self.vel*5
                self.y += self.vel*5
            else: 
                self.vel = self.vel * -1
        else: 
            if self.x - self.vel > self.pathx[0]:
                self.x += self.vel*5
                self.y += self.vel*5
            else: 
                self.vel = self.vel * -1
                
    def moveSq(self):                                                             ##Loop for moving in square
        if self.stage == 0:
            if self.x < self.pathx[1] + self.vel: 
                self.x += self.vel
            else:
                self.stage += 1
                
        elif self.stage == 1:
            if self.y < self.pathy[1]  + self.vel: 
                self.y += self.vel
            else:
                self.stage += 1
                
        elif self.stage == 2:
            if self.x > self.pathx[0] - self.vel: 
                self.x -= self.vel
            else:
                self.stage += 1
                
        elif self.stage == 3:
            if self.y > self.pathy[0] - self.vel: 
                self.y -= self.vel
            else:
                self.stage = 0
                
    def moveMaq(self):
        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            randomInt = random.randint(0,7)
            randomXY = random.randint(50, 200)
            if randomInt <= 1 and self.y > 100 :
                self.y -= 30
                print("dodge y -")
                
            elif randomInt <= 3 and randomInt >1 and self.y < 200:
                self.y += 30
                print("dodge y +")
                
            elif randomInt <= 5 and randomInt >3 and self.x < 200:
                self.x += 30
                print("dodge x +")
                
            elif randomInt <= 7 and randomInt >5 and self.x > 100:
                self.x -= 30
                print("dodge x -")
                
            if self.shield < 2:
                self.y = randomXY
                self.x = randomXY
                win.blit(maksiqImg[3], (self.x+20,self.y+40))
                win.blit(maksiqImg[3], (self.x-20,self.y+40))
                pygame.time.delay(50)
                
    def hit(self):
        global timeFin, winCon, highlight, isRecord
        if self.shield > 0:
            self.shield -= 1
            print("block")
            print("shield letf: " + str(self.shield))
        else:
            self.isDead = True
            self.x = 2000
            if self.etype == "Maksiq":
                fresh.play()
                timeFin = currentTime
                winCon = True
                with open("Rybols/Emulator_Tkinter/scores.txt", "a") as file:
                    date = datetime.datetime.now() 
                    date = str(date)
                    date = date[:16]
                    file.write(f'Time: {timeFin}s date: {date}\n')

                with open("Rybols/Emulator_Tkinter/scores.txt", "r") as file:
                    lines = file.read().splitlines()
                    values = []
                    for line in lines:
                        print(line)
                        match = re.search(r'Time: (\d+)s', line) ##digits between the Time: and s (including spaces)
                        if match:
                            values.append(int(match.group(1))) ##group one is the match so \d if we had more \d then more groups ## also int()
                    highlight = min(values)
                    if timeFin == highlight:
                        isRecord = True 
                    
                    
                
            
        
        


class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 7* facing
        self.range = 60
        
    def draw(self, win):
        win.blit(ball, (self.x - 5, self.y - 7))
        #pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
        
class Collider(object):
    def __init__(self, x, y, width, height, scene):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isHit = False
        self.scene = scene 
        
    def draw(self, win):                                                             
#        self.hitbox = (self.x, self.y, 24, 24) 
          #draws colliders!!!
        pygame.draw.rect(win, (0,255,0), (self.x, self.y, self.width, self.height), 2)  
        self.check(man)
        
    def check(self, character):
        self.isHit = False
        if character.x < self.x + self.width and character.x + character.width > self.x:
            if character.y < self.y + self.height and character.y  + character.height > self.y:
                self.isHit = True
                
class NPC(object):
    def __init__(self, x, y, width, height, scene, ntype):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scene = scene
        self.ntype = ntype
        self.isHit = False
        self.clicked = False
        
    def draw(self, win):  
        win.blit(npcImg[self.ntype], (self.x, self.y))
        #pygame.draw.rect(win, (0,255,0), (self.x, self.y, self.width, self.height), 2)  
        self.check(man)
        
    def check(self, character):
        self.isHit = False
        if character.x < self.x + self.width and character.x + character.width > self.x:
            if character.y < self.y + self.height and character.y  + character.height > self.y:
                self.isHit = True
                self.dialogue()
    
    def dialogue(self):
        global scene
        
        if  self.ntype == 1:
            win.blit(E, (self.x+5, self.y-15))
            if keys[pygame.K_e] and self.clicked == False:
                    sprint.play()
                    self.clicked = True
                    
        if self.ntype == 0:
            if self.scene == 0:
                win.blit(E, (self.x+5, self.y-15))
                if keys[pygame.K_e] and self.clicked == False:
                        puff.play()
                        self.clicked = True
                        pygame.mixer.music.set_volume(0)
            scene = 0
            self.scene = 0
       
                    
      
    def teleport(self, scene):
        self.scene = scene
        
 
class SceneChecker(object):
    def __init__(self, x, y, width, height, scene, side):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scene = scene 
        self.isHit = False
        self.side = side
        
    def draw(self, win):                                                             
        self.hitbox = (self.x, self.y, 24, 24) 
        #pygame.draw.rect(win, (0,255,0), (self.x, self.y, self.width, self.height), 2)
        win.blit(portal, (self.x, self.y, self.width, self.height))
        self.check(man)
        
    def check(self, character):
        global scene
        self.isHit = False
        if character.x < self.x + self.width and character.x + character.width > self.x:
            if character.y < self.y + self.height and character.y  + character.height > self.y:
                self.isHit = True  
                scene = self.scene 
                self.isHit = False
                drainggang.play()
                ##Teleport character to a midle of same side
                character.right = False
                character.left = False
                character.up = False
                character.down = False
                if self.side == 0:
                    character.x  = 50
                    character.y = windowHeight//2
                elif self.side == 1:
                    character.x  = 230
                    character.y = windowHeight//2
                elif self.side == 2:
                    character.y  = 50
                    character.x = windowWidth//2-50
                elif self.side == 3:
                    character.y  = 200
                    character.x = windowWidth//2
                    
                print(scene)

        
def redrawGameWindow():
    text = scoreFont.render('Rybols: ' + str(score), 1, (250,250,250))
    textTime = scoreFont.render('Time: ' + str(currentTime), 1, (250,250,250))
    textWin = scoreWin.render('! You Won !', 1, (100,255,0))
    textDie = scoreWin.render('! You Died !', 1, (250,0,0))
    textWin1 = scoreWin.render('Time: ' + str(timeFin), 1, (100,255,0))
    textWin2 = scoreWin.render('NEW RECORD ', 1, (255,0,0))
    textHigh = scoreWin.render('Best: ' + str(highlight), 1, (100,255,0))
    textShift = scoreFont1.render('Press Shift For Mushroom', 1, (250,250,250))
    win.blit(fullImg, (0,0))

    if scene == -2:
        win.fill(endscreen_color)
        man.draw(win)
        man.x = windowWidth//2 - 10
        man.y = windowHeight//2 
        win.blit(textDie, (40,50))
        
    if scene == -1:          
        
                                    ##Mainscene 
        win.blit(bgZERO, (0,0))  
        #win.blit(scoreImg, (-10,-20))
        
        
                
        #NPCS
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)
            
        
        
        man.draw(win)
    
    
    if scene == 0:          
                                    ##Mainscene 
        win.blit(bg[scene], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        ##Bullets
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (0,255,0), (35, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 225, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
            win.blit(rybolbol, (265,225))
            #pygame.draw.circle(win, (255,0,0), (280, 240), 15)
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
                
        #NPCS
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)
            
        #Objects with hitobox
        for collider in range(len(colliders)):
            if colliders[collider].scene == scene:
                colliders[collider].draw(win)  
            
        #Checks
        if len(deadEnemies) == len(enemiesInScene):  
            sceneNew2.draw(win)
        
            
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        
        man.draw(win)
            
    elif scene == 1:     
        ##POKEDEX SCENE 
        win.blit(ryboldex, (0,0)) 
        
        ind = 0
        row = 1
        for i in range(len(deadEnemies)):
            deadEnemies[i].pokeView = True
            deadEnemies[i].draw(win)
            collumn = 40 * ind
                
            if ind <= 4:
                hight = deadEnemies[i].height//8 
                deadEnemies[i].x = 24 + collumn
                deadEnemies[i].y = (48 * row) - hight
                ind +=1
                
            else:
                hight = deadEnemies[i].height//8 
                deadEnemies[i].x = 24 + collumn
                deadEnemies[i].y = (48 * row) - hight
                row += 1
                ind = 0
                
            
    elif scene == 2:
        win.blit(bg[scene-1], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        #Map
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (50,50,50), (35, 215, 9, 9))
        pygame.draw.rect(win, (0,255,0), (25, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 225, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
            win.blit(rybolbol, (265,225))
            #pygame.draw.circle(win, (255,0,0), (280, 240), 15)
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
       
        #NPCS
        puff.stop()
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)

        #Objects with hitobox
        for collider in range(len(colliders)):
            if colliders[collider].scene == scene:
                colliders[collider].draw(win)  
        
       #Checks
        if len(deadEnemies) == len(enemiesInScene):  
            sceneNew3.draw(win)
            sceneNew5.y = 230
            sceneNew5.draw(win)
         
        man.draw(win)
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        
    elif scene == 3:
        
        win.blit(bg[scene-1], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        #Map
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (50,50,50), (35, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 215, 9, 9))
        pygame.draw.rect(win, (0,255,0), (15, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 225, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
            win.blit(rybolbol, (265,225))
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
        
        #NPCS
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)
        
        #   Objects with hitobox
        for collider in range(len(colliders)):
            if colliders[collider].scene == scene:
                colliders[collider].draw(win)   

        #Checks
        #where to
        if len(deadEnemies) == len(enemiesInScene):  
            sceneNew4.x = 150
            sceneNew4.y = 230
            sceneNew4.side = 2
            sceneNew4.draw(win)
        
        man.draw(win)
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
            
        
    elif scene == 4:
        
        win.blit(bg[scene-1], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (50,50,50), (35, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 215, 9, 9))
        pygame.draw.rect(win, (0,255,0), (15, 225, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
            win.blit(rybolbol, (265,225))
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
        #Objects with hitobox
        for collider in range(len(colliders)):
            if colliders[collider].scene == scene:
                colliders[collider].draw(win)  
        #NPCS
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)
        
        #Checks
        #where to
        
        if len(deadEnemies) >= len(enemiesInScene): 
            sceneNew3.x = 100
            sceneNew3.y = 0
            sceneNew3.draw(win)
            sceneNew5.x = 270
            sceneNew5.y = 160
            sceneNew5.side = 0
            sceneNew5.draw(win)
            if len(deadEnemies) >= len(enemies)-2: 
                sceneNew6.y = 230
                sceneNew6.draw(win)
            
        man.draw(win)
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
            
    elif scene == 5:
        
        win.blit(bg[scene-1], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (50,50,50), (35, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 225, 9, 9))
        pygame.draw.rect(win, (0,255,0), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
            win.blit(rybolbol, (265,225))
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
        
        #NPCS
        for npc in range(len(npcs)):
            if npcs[npc].scene == scene:
                npcs[npc].draw(win)

        #Objects with hitobox
        for collider in range(len(colliders)):
            if colliders[collider].scene == scene:
                colliders[collider].draw(win)  
        #Checks
        #where to
        
        if len(deadEnemies) == len(enemiesInScene): 
            sceneNew4.x = 0
            sceneNew4.y = 85
            sceneNew4.side = 1
            sceneNew4.draw(win)
            
        man.draw(win)
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
        
    elif scene == 6:
        if isFullscreen == True:
            win.blit(ryboldex, (windowWidth+5,-5))
            ind = 0
            row = 1
            for i in range(len(deadEnemies)):
                deadEnemies[i].pokeView = True
                deadEnemies[i].draw(win)
                collumn = windowWidth + (40 * ind)
                    
                if ind <= 4:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    ind +=1
                    
                else:
                    hight = deadEnemies[i].height//8 
                    deadEnemies[i].x = 24 + collumn
                    deadEnemies[i].y = (48 * row) - hight
                    row += 1
                    ind = 0
        
        
        win.blit(bg[scene-1], (0,0))  
        #win.blit(scoreImg, (-10,-20))
        
        for bullet in bullets:
            bullet.draw(win)
        ##GUI
        #Map
        win.blit(mapBoard, (5,205))
        pygame.draw.rect(win, (50,50,50), (35, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 215, 9, 9))
        pygame.draw.rect(win, (50,50,50), (15, 225, 9, 9))
        pygame.draw.rect(win, (50,50,50), (25, 225, 9, 9))
        pygame.draw.rect(win, (255,0,0), (15, 235, 9, 9))
        
        if shootBullet == False:
           win.blit(rybolbol, (265,225))
        ##Enemies    
        for i in range(len(enemies)):
            if enemies[i].isDead == False and enemies[i].scene == scene:                                           ##If enemy is not dead display him
                enemies[i].draw(win)
        #Checks
        #where to
        
        #if len(deadEnemies) == len(enemiesInScene):  
            #sceneNew1.draw(win)
        
        man.draw(win)
        win.blit(timeBoard, (0, 0))
        win.blit(text, (1,1))
        
        if not keys[pygame.K_LSHIFT]:
            shiftTxt = win.blit(textShift, (90,25))
            shiftTxt.x = -50
            
        win.blit(timeBoard, (210, 2))
        win.blit(textTime, (222,2))
        x_life = 125
        for life in range(man.life):
            win.blit(heart, (x_life, 10))
            x_life += 11
        
        if winCon:
            man.x = windowWidth//2 - 10
            man.y = windowHeight//2 - 20
            win.blit(textWin, (50,50))
            win.blit(textWin1, (50,125))
            win.blit(textHigh, (50, 200))
            if isRecord:
                win.blit(textWin2, (30, 0))
        else:
            win.blit(textTime, (220,0))
            
        
        
    pygame.display.update()
     
#mainloop
#main character
scoreFont = pygame.font.SysFont('Impact', 20, False, True)
scoreFont1 = pygame.font.SysFont('Impact', 12, False, True)
scoreWin = pygame.font.SysFont('Impact', 50, False, False)
man = Player(215,90, 24, 24)


#enemies
rybolend = Enemy(10, 0, 24, 32, 210, "SQr", 3, 0)

kaneki = Enemy( 100, 50, 24, 32, 20, "LR", 0, 0)
kaneki1 = Enemy(random.randint(70,110), random.randint(50,150), 24, 32, 30, "LR", random.randint(2,3), 0)
kaneki2 = Enemy(random.randint(70,110), random.randint(50,150), 24, 32, 5, "LR", random.randint(2,3), 0)
kaneki3 = Enemy(random.randint(70,110), random.randint(50,150), 24, 32, random.randint(0,30), "LR", random.randint(2,5), 0)
kaneki4 = Enemy(random.randint(70,110), random.randint(50,150), 24, 32, random.randint(0,20), "LR", random.randint(2,5), 0)
kaneki5 = Enemy(random.randint(70,150), random.randint(50,150), 24, 32, random.randint(10,50), "LR", random.randint(2,4), 0)

kanekiend = Enemy(0, 0, 24, 32, 250, "LRr", 4, 0)

rybol = Enemy(100, 100, 24, 32, 100, "SQ", 0, 0)
mword = Enemy(50, 100, 24, 32, 100, "Pix", 5, 0)
rybol5 = Enemy(0, 100, 24, 32, 100, "SQ", 0, 0)

rybol1 = Enemy(100, 50, 24, 32, 35, "SQ", 2, 0)
rybol2 = Enemy(random.randint(130,140), random.randint(50,200), 24, 32, 12, "SQ", 5, 0)
rybol3 = Enemy(random.randint(130,140), random.randint(50,200), 24, 32, 16, "SQ", 5, 0)
rybol4 = Enemy(random.randint(130,140), random.randint(100,200), 24, 32, 12, "SQ", 5, 0)
rybol5 = Enemy(random.randint(130,140), random.randint(50,100), 24, 32, 16, "SQ", 5, 0)


don = Enemy(100, 160, 40, 40, 10, "LRDon", 2, 1)
maksiq = Enemy(140,100, 40, 40, 0, "Maksiq",6, 4)

bullets = []
enemies = [rybolend, kaneki, kaneki1, kaneki2, kaneki3, kaneki4, kaneki5, rybol1, rybol2, rybol3, rybol4, rybol5, mword, rybol5, rybol, don, maksiq, kanekiend]

mucher = NPC(280, 100, 24, 32, -1, 0)
mucher2 = NPC(110, 200, 24, 32, 4, 1)


npcs = [mucher, mucher2]

#Checks for the dead enemiesP{added when hit}


    
deadEnemies = []
enemiesInScene = []  
#objects with hitboxes

house = Collider(0,35,50,50, 0)
house1 = Collider(0,200,50,50, 0)
house2 = Collider(190,25,100, 60, 0)
house3 = Collider(120, 160, 170, 110, 0)
house4 = Collider(0,35,50,50, 2)
house5 = Collider(0,0,50,300, 3)
sea = Collider(140,0,200,300, 5)
colliders = [house, house1, house2, house3, house4, house5, sea]

#checks
#in order 
wh = 15
sceneNew2 = SceneChecker(0,100,wh,wh, 2, 1)
sceneNew3 = SceneChecker(0,100,wh,wh, 3, 1)
sceneNew5 = SceneChecker(200,215,wh,wh, 5, 2)

sceneNew4 = SceneChecker(200,215,wh,wh, 4, 2)
sceneNew6 = SceneChecker(120,215,wh,wh, 6, 3)
sceneNew1 = SceneChecker(130,0,wh,wh, 0, 0)

currentTime = 0
run = True
while run:
    clock.tick(18)
    
    currentTime = pygame.time.get_ticks()//1000

    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and fullClicked == False:
                win = pygame.display.set_mode((windowHeight, windowWidth), pygame.FULLSCREEN)
                isFullscreen = True
                fullClicked = True
            elif event.key == pygame.K_f and fullClicked == True:
                win = pygame.display.set_mode((windowWidth, windowHeight))
                isFullscreen = False
                fullClicked = False
                
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.QUIT:
            run = False
            
            
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_p:
#                
#                if scene == 0:  
#                    print("Pokedex")
#                    man.right = False
#                    man.left = False
#                    man.up = False
#                    man.down = False
#                    canRight = False
#                    canLeft = False
##                    canUp = False
#                    canDown = False
 #                   scene = 1
                    
#                elif scene == 1:
#                    man.right = False
#                    man.left = False
#                    man.up = False
#                    man.down = False
#                    canRight = True
 #                   canLeft = True
#                    canUp = True
 #                   canDown = True
  #                  scene = 0
                    
                    
    for i in range(len(enemies)):
        if enemies[i].scene == scene and enemies[i] not in enemiesInScene :
            enemiesInScene.append(enemies[i])      
    
    for bullet in bullets:
        ##ENEMIES COLISION CHECK /it goes throught the list of enemies and if something is inside of it it check for a hitbox
        for i in range(len(enemies)):
            if enemies[i].scene == scene:
                if bullet.y - bullet.radius < enemies[i].hitbox[1] + enemies[i].hitbox[3] and bullet.y + bullet.radius > enemies[i].hitbox[1]:
                    if bullet.x + bullet.radius > enemies[i].hitbox[0] and bullet.x - bullet.radius < enemies[i].hitbox[0]  + enemies[i].hitbox[2] and enemies[i].isDead == False:
                        if enemies[i].isDead:
                            print("in list")
                        elif enemies[i].shield > 0:
                            enemies[i].hit()
                            if bullet in bullets:
                                bullets.pop(bullets.index(bullet))
                            shootBullet = False
                        else:
                            enemies[i].hit()
                            score += 1
                            
                            deadEnemies.append(enemies[i])
                            print(enemies)
                            
                            if bullet in bullets:
                                bullets.pop(bullets.index(bullet))
                            shootBullet = False
                            
                    
            
        if man.right or man.left: 
            if bullet.x < man.x + bullet.range and bullet.x > man.x - bullet.range:
                bullet.x += bullet.vel
                canUp = False
                canDown = False
                
            else:
                canUp = True
                canDown = True
                shootBullet = False
                if bullet in bullets:
                    bullets.pop(bullets.index(bullet))
                
        if man.up or man.down:
            if bullet.y < man.y + bullet.range and bullet.y > man.y - bullet.range:
                bullet.y += bullet.vel
                canLeft = False
                canRight = False
                
            else:
                canLeft = True
                canRight = True
                shootBullet = False
                if bullet in bullets:
                    bullets.pop(bullets.index(bullet))
                
        if man.down == False and man.right == False and man.up == False and man.left == False:
            if bullet.x < man.x + bullet.range and bullet.x > man.x - bullet.range:
                bullet.x += bullet.vel
                canUp = False
                canDown = False
                
            else:
                canUp = True
                canDown = True
                shootBullet = False
                if bullet in bullets:
                    bullets.pop(bullets.index(bullet))
                
    keys = pygame.key.get_pressed()
    
    ##Checks colliders 
    for collider in range(len(colliders)):   
        if colliders[collider].isHit == True:
            if man.left:
                man.x = colliders[collider].x + colliders[collider].width + 10
                
            elif man.right:
                man.x = colliders[collider].x - 25
                
            elif man.up:
                man.y = colliders[collider].y + colliders[collider].height + 10
                
            elif man.down:
                man.y = colliders[collider].y - 25
                  
    if keys[pygame.K_LSHIFT]  and scene == 6:
        man.isShield = True
        
        
    if keys[pygame.K_p] and isFullscreen == False:
        pygame.time.delay(100)
        if scene != 1:
            tempscene = scene
            scene = 1
        elif scene == 1:
            scene = tempscene
            
            
    if keys[pygame.K_i]: 
        pygame.time.delay(200)
        print(str(man.x) + " man x")
        print(str(man.y) + " man y")
        print(str(scene) + "scene nr")
        print("bullets:")
        print(enemiesInScene)
        print(len(enemies))
        print(len(deadEnemies))
    
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        elif man.right:
            facing = 1
        elif man.up:
            facing = -1
        else: 
            facing = 1
            
        shootBullet = True
        if len(bullets) < 1 and canShoot == True and man.isShield == False:
            bullets.append(Projectile( man.x + 12, man.y + 12, 8, (202,69,211), facing))
        
    if keys[pygame.K_LEFT] and man.x>man.vel and canLeft:
            man.x -= man.vel
            man.right = False
            man.left = True
            man.up = False
            man.down = False
            man.isStanding = False
            
            for bullet in bullets:
                bullet.x += 5
        
    elif keys[pygame.K_RIGHT] and man.x < windowWidth - man.vel - man.width and canRight:
            man.x += man.vel
            man.right = True
            man.left = False
            man.up = False
            man.down = False
            man.isStanding = False
            
            for bullet in bullets:
                bullet.x -= 5
            
    elif keys[pygame.K_UP] and man.y > man.vel and canUp:
            man.y -=  man.vel
            man.right = False
            man.left = False
            man.up = True
            man.down = False
            man.isStanding = False
            
            for bullet in bullets:
                bullet.y += 5
        
    elif keys[pygame.K_DOWN] and man.y < windowHeight - man.vel - man.height and canDown:
            man.y += man.vel
            man.right = False
            man.left = False
            man.up = False
            man.down = True
            man.isStanding = False
            
            for bullet in bullets:
                bullet.y -= 5
        
    else:
        man.isStanding = True
            
        




#    else: 
#        man.right = False
#        man.left = False
#        man.up = False
#        man.down = False
        
    
    redrawGameWindow()
    
pygame.quit()