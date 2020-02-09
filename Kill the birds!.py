#15-112: Fundementals of Programming and Computer Science
#Final Project
#Name: Andrew Edward
#AndrewID: aedward

import pygame
from pygame.locals import *
import Tkinter
from PIL import ImageTk, Image
import sys
import random


#The code is composed of several functions for windows like Menu(): the main window that appears once you open the game, how():
#how to play window, getback(): helper function for how() to return to main menu when "back" button is clicked
#play(): which is the main pygame window for the whole game, the play contains all of the levels, main constants and functions like collision detection...etc

#The game also consists of classes for different objects to maintain simplicity such as
#spaceship(): for the player, birds(): class for birds, EGG(): class for eggs thrown by the the birds, Boss(): class for the leader bird



#___________________________________________________________________________________________________________
#MAIN MENU WINDOW

def menu():

    root = Tkinter.Tk()
    root.geometry("1024x768")

    #get background image and place it
    background = ImageTk.PhotoImage(Image.open("Images/menu_galaxy.png"))
    background_label = Tkinter.Label(root, image = Background)
    background_label.place(x=0,y=0,relwidth=1,relheight=1)

    #Buttons, and they labels
    play_Btn_Image = ImageTk.PhotoImage(Image.open("Images/button_play.png"))
    how_Btn_Image = ImageTk.PhotoImage(Image.open("Images/button_howtoplay.png"))
    playBtn = Tkinter.Button(root, image = play_Btn_Image, borderwidth=0, command=lambda x=root:play(x))
    howBtn = Tkinter.Button(root, image = how_Btn_Image, borderwidth=0, command=lambda x=root:how(x))

    #pack buttons
    playBtn.pack(pady=(300,5))
    howBtn.pack(pady=50)

    root.mainloop()
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#HOW TO PLAY WINDOW

def how(close):
    #close the main menu
    close.destroy()
    #load the new window
    root = Tkinter.Tk()
    root.geometry("1024x768")

    #get background image and place it
    background = ImageTk.PhotoImage(Image.open("Images/menu_howtoplay.png"))
    background_label = Tkinter.Label(root, image = Background)
    background_label.place(x=0,y=0,relwidth=1,relheight=1)

    #place the instructions image
    #HOW_TO_PLAY = Image.open("Images/howtoplay.png")
    #HOW_TO_PLAY = HOW_TO_PLAY.resize((900,600))
    #HOW_TO_PLAY = ImageTk.PhotoImage(HOW_TO_PLAY)
    #HOW_TO_PLAYLabel = Tkinter.Label(root, image = HOW_TO_PLAY , borderwidth=0, width = 900, height = 600)
    #HOW_TO_PLAYLabel.photo = HOW_TO_PLAY

    Back_Btn_Image = ImageTk.PhotoImage(Image.open("Images/button_back.png"))
    BackBtn = Tkinter.Button(root, image =Back_Btn_Image, borderwidth=0, command=lambda x=root:getback(x))

    #pack instructions label
    #HOW_TO_PLAYLabel.pack(pady=(20,5))
    BackBtn.pack(pady=(650,0))

    root.mainloop()
#function to re-create a menu when "back" button is clicked
def getback(x):
    x.destroy()
    menu()

#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#class for spaceship (player)
    
class Spaceship(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        #save to images for the spaceship, one when it's not moving, other when a button is clicked
        self.static = pygame.image.load("Images/sprite_static.png").convert_alpha()
        self.moving = pygame.image.load("Images/sprite_active.png").convert_alpha()
        self.heart = pygame.image.load("Images/Hearts.png").convert_alpha()
        self.image = self.static
        self.rect = self.image.get_rect()
        #for location of image
        self.rect.x = x
        self.rect.y = y
        self.surface = screen
        #amount of points the spaceship moves
        self.dist=15
        self.lives=3

    def movements(self):

        #if the Right key is pressed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.image = self.moving
            #to be sure the spaceship is always inside the window
            if self.rect.x < 920:
                self.rect.x = self.rect.x + self.dist

        #if the LEFT key is pressed
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            #flips the image (((1)))
            self.image = pygame.transform.flip(self.moving,1,0)
            #to be sure the spaceship is always inside the window
            if self.rect.x != 0:
                self.rect.x = self.rect.x - self.dist
        elif pygame.key.get_pressed()[pygame.K_UP]:
            #flips the image (((1)))
            self.image = self.static
            #to be sure the spaceship is always inside the window
            if self.rect.y != 0:
                self.rect.y = self.rect.y - self.dist
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            #flips the image (((1)))
            self.image = self.static
            #to be sure the spaceship is always inside the window
            if self.rect.y < 600:
                self.rect.y = self.rect.y + self.dist
        #if no key is pressed
        elif pygame.event.get()==[]:
            self.image = self.static

    #draws the object on the screen
    def draw(self,surface):
        self.surface.blit(self.image, self.rect)
        for i in range(self.lives):
            self.surface.blit(self.heart,((i*50),50))
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#class for laser            

class Laser(pygame.sprite.Sprite): #I know it's a rocket but until I find a good quality laser picture
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)

        #load the picture of the laser
        self.image = pygame.image.load("Images/laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        #for location of laser
        self.rect.x = x
        self.rect.y = y
        #distance travelled by laser
        self.dist = 15
        self.surface = screen
        #constant to be used to identify when a bullet is no longer on screen
        self.OutOfRange = False

    #draws the object on screen
    def draw(self):
        self.surface.blit(self.image, self.rect)


    def update(self):
        #check if laser beam is not out of screen
        if self.rect.y > 0:
            self.rect.y = self.rect.y - self.dist
        #if it's out, chang e outofange to True
        else:
            self.OutOfRange = True
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#class for the evil birds!
            
class birds(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        #load the picture of bird
        self.image = pygame.image.load("Images/bird_static.png").convert_alpha()
        self.moving = pygame.image.load("Images/bird_active.png").convert_alpha()
        self.static = pygame.image.load("Images/bird_static.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        #for location of bird
        self.dist = 1
        self.rect.x = x
        self.rect.y = y
        self.origX = x
        self.origY = y
        self.newX = self.dist
        self.newY = self.dist
        self.surface = screen
        self.dead = False
        self.counter = 0

    #draws the object on screen
    def draw(self):
        self.surface.blit(self.image, self.rect)
        if self.rect.x < 920:
            self.image = self.moving
            self.counter = self.counter + 1
            if self.counter%4 == 0:
                self.image = self.static

        elif self.rect.x <= 0 and self.rect.x < 920:
            self.image = self.moving
            self.counter = self.counter + 1
                    
    def update(self):
        #if the bird is dead, move outside
        if self.dead == True:
            self.rect.x = 4000
            self.rect.y = 4000
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#Class for eggs coming from evil birds

class EGG(pygame.sprite.Sprite): 
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)

        #load the picture of the egg
        self.image = pygame.image.load("Images/small_egg.png").convert_alpha()
        self.rect = self.image.get_rect()
        #for position of egg
        self.rect.x = x
        self.rect.y = y
        #distance travelled by egg
        self.dist = 10
        self.surface = screen
        #constant to be used to identify when a egg is no longer on screen
        self.OutOfRange = False

    #draws the object on screen
    def draw(self):
        self.surface.blit(self.image, self.rect)


    def update(self):
        #check if egg is not out of screen
        if self.rect.y < 800:
            self.rect.y = self.rect.y + self.dist
        #if it's out, change outofrange to True
        else:
            self.OutOfRange = True
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#class for the BOSS!
            
class Boss(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        #load the picture of the boss in active and static status
        self.image = pygame.image.load("Images/boss_static.png").convert_alpha()
        self.moving = pygame.image.load("Images/boss_active.png").convert_alpha()
        self.static = pygame.image.load("Images/boss_static.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        #for location of boss
        self.dist = 1
        self.rect.x = x
        self.rect.y = y
        self.origX = x
        self.origY = y
        self.surface = screen
        self.dead = False
        #for the movement of wings
        self.counter = 0
        #boss health
        self.HP = 0

    #draws the object on screen
    def draw(self):
        self.surface.blit(self.image, self.rect)
        if self.rect.x < 920:
            self.image = self.moving
            self.counter = self.counter + 1
            if self.counter%4 == 0:
                self.image = self.static
                    
    def update(self):
        #if hp is = 10, means he is dead
        if self.HP == 10:
            #move out of screen
            self.dead = True
            self.rect.x = 4000
            self.rect.y = 4000
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#MAIN GAME WINDOW

def play(close):
    #close the main menu
    close.destroy()

    #call pygame
    pygame.init()

    #Constants
    FPS=60
    WHITE = (255, 255, 255)
    OFF = 2
    LIVE = 0
    status = LIVE
    current_Score = 0
    level = 1
    cSText = pygame.font.SysFont('Arial Black',20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
    level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL 1', True, pygame.color.Color('Red'))
    game_over_Text = pygame.font.SysFont('Arial Black', 20).render('GAME OVER', True, pygame.color.Color('Red'))
    winText = pygame.font.SysFont('Arial Black', 50).render('YOU WON!', True, pygame.color.Color('Green'))
    boss_level_Text = pygame.font.SysFont('Arial Black', 20).render('Shoot the boss 10 times to kill him!', True, pygame.color.Color('White'))
    game_over = 0
    TIMER = 1000 + level*500
    
    #for FPS
    clock = pygame.time.Clock()

    #elements of game
    screen = pygame.display.set_mode((1024,768),0,32)
    pygame.display.set_caption('Kill the birds!')
    background=pygame.image.load("Images/galaxy.png")
    screen.fill(WHITE)
    player = Spaceship(screen,450,600)
    BOSS = Boss(screen,400,50)

    #-------------------------------------------------------------------------------
    #levels and backups [credit for the leveling system to Hari]
    levels = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

              2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

              3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                  birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

              4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                  birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                  birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                  birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
              5:[[Boss(screen,400,50)],0]}

    levels1 = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

               2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

               3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                   birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

               4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                   birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                   birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                   birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
               5:[[Boss(screen,400,50)],0]}

    levels2 = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

               2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

               3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                   birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

               4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                   birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                   birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                   birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
               5:[[Boss(screen,400,50)],0]}


    levels3 = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

               2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

               3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                   birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

               4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                   birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                   birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                   birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
               5:[[Boss(screen,400,50)],0]}



    levels4 = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

              2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

              3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                  birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

              4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                  birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                  birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                  birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
              5:[[Boss(screen,400,50)],0]}

              
    levels5 = {1:[[birds(screen,400,50),birds(screen,200,50)],0],

               2:[[birds(screen,200,50),birds(screen,300,50),birds(screen,400,50),birds(screen,500,50),birds(screen,600,50),birds(screen,700,50)],0],

               3:[[birds(screen,200,80),birds(screen,300,80),birds(screen,400,80),birds(screen,500,80),birds(screen,600,80),birds(screen,700,80),
                   birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20)],0],

               4:[[birds(screen,200,20),birds(screen,300,20),birds(screen,400,20),birds(screen,500,20),birds(screen,600,20),birds(screen,700,20),
                   birds(screen,250,80),birds(screen,350,80),birds(screen,450,80),birds(screen,550,80),birds(screen,650,80),
                   birds(screen,300,140),birds(screen,400,140),birds(screen,500,140),birds(screen,600,140),
                   birds(screen,350,200),birds(screen,450,200),birds(screen,550,200)],0],
              
               5:[[Boss(screen,400,50)],0]}


    #backups and lists
    lasers_list = []
    eggs_list = []
    birds_list = levels[1][0]
    killed_birds = levels1[1][0]
    killed_birds1 = levels2[1][0]
    killed_birds2 = levels3[1][0]
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    #starting:
    level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('White')) 
    screen.blit(background,(0,0))
    screen.blit(cSText,(0,0))
    screen.blit(level_Text,(430,350))
    player.draw(screen)
    
    pygame.display.update()


    pygame.time.delay(4000)

    #------------------------------------------------------------------------
    #Main loop 
    
    while True and player.lives != 0:

        for event in pygame.event.get():

            #if event is quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #if a space is clicked, it begins firing laser
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                if lasers_list == []:
                    laser = Laser(screen, player.rect.x+45,player.rect.y)
                    lasers_list = lasers_list + [laser]


        #------------------------------------------------------------------------
        #if game is on
                    
        if status == LIVE:

            #code for keyboard keys to work
            player.movements()

            #handles movement of laser
            for i in lasers_list:

                i.update()

                #if the laser beam is out of range, remove from list
                if i.OutOfRange == True:
                    lasers_list.remove(i)

            #if its already level 5, show the boss
            if level == 5:

                BOSS.draw()
                BOSS.update()
    
                for i in lasers_list:

                    if pygame.sprite.collide_rect(BOSS,i):

                        #make the condition true so you can remove the object
                        BOSS.HP = BOSS.HP + 1
                        lasers_list.remove(i)

                        if BOSS.HP == 10:
                            BOSS.update()
                            current_Score = current_Score + 1
                            cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                            screen.blit(cSText,(0,0))

                #checks for collisions between the boss and the player       
                if pygame.sprite.collide_rect(BOSS,player):
                    player.lives = player.lives - 1
                    eggs_list = []
                    #if player has lives remaining, restart the level
                    if player.lives!=0:

                        #reset timer
                        TIMER = 1000 + level*500
                        TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('Red'))
                        #reset score
                        current_Score = 0
                        cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                        screen.blit(background,(0,0))
                        screen.blit(cSText,(0,0))
                        #reset player position
                        player.rect.x = 450
                        player.rect.y = 600
                        level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('Red')) 
                        screen.blit(level_Text,(430,350))
                        boss_level_Text = pygame.font.SysFont('Arial Black', 20).render('Shoot the boss 10 times to kill him!', True, pygame.color.Color('White'))
                        screen.blit(boss_level_Text,(300,400))
                        pygame.display.update()
                        pygame.time.delay(4000)

                #if timer is lower than 0, then it time ran out
                if TIMER <= 0:
                    player.lives = player.lives - 1
                    eggs_list = []

                    #if player has lives remaining, restart the level
                    if player.lives!=0:

                        #reset timer
                        TIMER = 1000 + level*500
                        TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('Red'))
                        #reset score
                        current_Score = 0
                        cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                        screen.blit(background,(0,0))
                        screen.blit(cSText,(0,0))
                        #reset player position
                        player.rect.x = 450
                        player.rect.y = 600
                        level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('Red')) 
                        screen.blit(level_Text,(430,350))
                        boss_level_Text = pygame.font.SysFont('Arial Black', 20).render('Shoot the boss 10 times to kill him!', True, pygame.color.Color('White'))
                        screen.blit(boss_level_Text,(300,400))
                        pygame.display.update()
                        pygame.time.delay(4000)

                        #keep backups updated and update birds positions
                        if levels1[level][1] != 1:
                            birds_list = killed_birds

                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels1[level][1]=1

                        elif levels2[level][1]!=1:
                            birds_list = killed_birds1

                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels2[level][1]=1

                        elif levels3[level][1]!=1:
                            birds_list = killed_birds2
                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels3[level][1]=1
                            levels = levels3
                            
                    #if player has no more lives
                    if player.lives == 0:
                        #quit
                        game_over_Text = pygame.font.SysFont('Arial Black', 20).render('GAME OVER', True, pygame.color.Color('White'))
                        screen.blit(game_over_Text,(430,350))
                        pygame.quit()
                        Menu()
    
            #if it isn't level 5, keep going
            #update interface
            screen.blit(background,(0,0))
            screen.blit(cSText,(0,0))
            player.draw(screen)

            #initialize birds
            for i in birds_list:
                i.draw()

                if i.dead == True:
                    birds_list.remove(i)

            #for every time the timer%50 == 0, add an egg
            if TIMER%50 == 0:
                #if there are birds
                if birds_list != []:
                    #if no eggs on the screen
                    if eggs_list == []:
                        #choose a random bird
                        c = int(random.choice(range(0,len(levels[level][0]))))
                        #throw an egg from that bird                            
                        q = EGG(screen,levels[level][0][c].rect.x+20,levels[level][0][c].rect.y+20)

                        #if its level 5, make eggs bigger
                        if level == 5:
                            #get a random x,y position as long as it is inside of bird
                            randomX_position = random.choice(range(levels[level][0][0].rect.x,levels[level][0][0].rect.x+200,10))
                            randomY_position = random.choice(range(levels[level][0][0].rect.y,levels[level][0][0].rect.y+200,10))
                            q = EGG(screen,randomX_position,randomY_position)
                            q.image = pygame.image.load("Images/big_egg.png").convert_alpha()
                        #increase speed of eggs according to each level
                        q.dist = q.dist + level*3
                        eggs_list = eggs_list + [q]
                    
            #handles eggs movement
            for egg in eggs_list:
                if birds_list != []:
                    egg.draw()
                    #if egg is out of the screen, remove from list
                    if egg.OutOfRange == True:
                        eggs_list.remove(egg) 
            #------------------------------------------------------------------------

            for bird in birds_list:  
                #for each bird check if it collides with player
                if pygame.sprite.collide_rect(player,bird):
                    #if a collision happen, player loses a life
                    player.lives = player.lives - 1
                    eggs_list = []

                    #if player has lives remaining, restart the level
                    if player.lives!=0:
                        lasers_list = []
                        #reset timer
                        TIMER = 1000 + level*500
                        TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('Red'))
                        #reset score
                        current_Score = 0
                        cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                        screen.blit(background,(0,0))
                        screen.blit(cSText,(0,0))
                        #reset player position
                        player.rect.x = 450
                        player.rect.y = 600
                        level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('White')) 
                        screen.blit(level_Text,(430,350))
                        pygame.display.update()
                        pygame.time.delay(4000)

                #if time runs out
                if TIMER <= 0:
                    player.lives = player.lives - 1
                    eggs_list = []

                    #if player has lives remaining, restart the level
                    if player.lives!=0:
                        lasers_list = []
                        #reset timer
                        TIMER = 1000 + level*500
                        TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('Red'))
                        #reset score
                        current_Score = 0
                        cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                        screen.blit(background,(0,0))
                        screen.blit(cSText,(0,0))
                        #reset player position
                        player.rect.x = 450
                        player.rect.y = 600
                        level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('White')) 
                        screen.blit(level_Text,(430,350))
                        pygame.display.update()
                        pygame.time.delay(4000)

                        #update backups and birds
                        if levels1[level][1] != 1:
                            birds_list = killed_birds

                            for j in birds_list:
                                j.rect.x = j.origX
                                j.rect.y = j.origY
                            levels1[level][1]=1

                        elif levels2[level][1]!=1:
                            birds_list = killed_birds1

                            for j in birds_list:
                                j.rect.x = j.origX
                                j.rect.y = j.origY
                            levels2[level][1]=1

                        elif levels3[level][1]!=1:
                            birds_list = killed_birds2
                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels3[level][1]=1
                            levels = levels3
                        

                    #if player has no lives, quit
                    if player.lives == 0:

                        game_over_Text = pygame.font.SysFont('Arial Black', 20).render('GAME OVER', True, pygame.color.Color('White'))
                        screen.blit(game_over_Text,(0,0))
                        pygame.quit()
                        menu()
                        
                #------------------------------------------------------------------------


                #------------------------------------------------------------------------
                #initialize laser
                for i in lasers_list:
                    i.draw()

                #check for colleation
                for i in lasers_list:

                        if pygame.sprite.collide_rect(bird,i):
                            #make the condition true so you can remove the object and laser
                            bird.dead = True
                            lasers_list.remove(i)
                            birds_list.remove(bird)
                            killed_birds.append(bird)
                            #add 1 to the score
                            current_Score = current_Score + 1
                            cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                            screen.blit(cSText,(0,0))
            
            #update eggs
            for egg in eggs_list:

                if birds_list != []:
                    egg.draw()
        
                    if egg.OutOfRange == True:
                        eggs_list.remove(egg)
                    egg.update()


                    
            for egg in eggs_list:

                #check for collision between player and egg
                if pygame.sprite.collide_rect(player,egg):
                    #make the condition true so you can remove the object
                    egg.OutOfRange = True
                    eggs_list.remove(egg)
                    player.lives = player.lives - 1

                    if player.lives!=0:
                        lasers_list = []
                        #reset timer
                        TIMER = 1000 + level*500
                        TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('Red'))
                        #reset score
                        current_Score = 0
                        cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                        screen.blit(background,(0,0))
                        screen.blit(cSText,(0,0))
                        #reset player position
                        player.rect.x = 450
                        player.rect.y = 600
                        level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('White')) 
                        screen.blit(level_Text,(430,350))
                        pygame.display.update()
                        pygame.time.delay(4000)

                        #update backups and birds
                        if levels1[level][1]!=1:
                            birds_list = killed_birds

                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                                eggs_list = []
                            levels1[level][1]=1
                            levels = levels1

                        elif levels2[level][1]!=1:
                            birds_list = killed_birds1

                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels2[level][1]=1
                            levels = levels2

                        elif levels3[level][1]!=1:
                            birds_list = killed_birds2
                            for j in birds_list:
                                j.rect.x=j.origX
                                j.rect.y=j.origY
                            levels3[level][1]=1
                            levels = levels3


                    #if player has no lives left, quit
                    if player.lives == 0:
                        game_over_Text = pygame.font.SysFont('Arial Black', 20).render('GAME OVER', True, pygame.color.Color('White'))
                        screen.blit(game_over_Text,(0,0))
                        pygame.quit()
                        menu()
                
                

            #if birds list is empty, that means a level is over
            if birds_list == []:

                #if this was level 5, then you won
                if level==5:
                    screen.blit(winText,(400,350))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    pygame.quit()
                    menu()
                    game_over = 1

                #if it was level 4, then load the boss
                if level == 4:
                    eggs_list = []
                    screen.blit(background,(0,0))
                    screen.blit(cSText,(0,0))
                    player.rect.x = 450
                    player.rect.y = 600
                    level = level + 1
                    level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('Red'))
                    current_Score = 0
                    cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                    screen.blit(level_Text,(430,350))
                    boss_level_Text = pygame.font.SysFont('Arial Black', 20).render('Shoot the boss 10 times to kill him!', True, pygame.color.Color('White'))
                    screen.blit(boss_level_Text,(350,500))
                    TIMER = 1000 + level*500
                    TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('White'))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    birds_list = levels[level][0]
                    killed_birds = levels1[level][0]
                    killed_birds1 = levels2[level][0]

                #else, keep going with the lists you got
                if level == 1 or level == 2 or level == 3:
                    eggs_list = []
                    screen.blit(background,(0,0))
                    screen.blit(cSText,(0,0))
                    player.rect.x = 450
                    player.rect.y = 600
                    level = level + 1
                    level_Text = pygame.font.SysFont('Arial Black', 50).render('LEVEL '+str(level), True, pygame.color.Color('Red'))
                    current_Score = 0
                    cSText = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                    screen.blit(level_Text,(430,350))
                    TIMER = 1000 + level*500
                    TIMER_Text = pygame.font.SysFont('Arial Black', 50).render('TIMER'+str(TIMER), True, pygame.color.Color('White'))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    birds_list = levels[level][0]
                    killed_birds = levels1[level][0]
                    killed_birds1 = levels2[level][0]

        #if game is not over, keep updating
        if game_over != 1:
            curScore_text = pygame.font.SysFont('Arial Black', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
            screen.blit(cSText,(0,0))

            #if statement for timer, keep decreasing until it's less than 0
            if TIMER >= 0:
                TIMER = TIMER - 3
                                
            TIMER_Text = pygame.font.SysFont('Arial Black', 20).render('TIMER: '+ str(TIMER), True, pygame.color.Color('White'))
            screen.blit(TIMER_Text,(880,0))

            #update everything
            pygame.display.flip()
            clock.tick(60)
#___________________________________________________________________________________________________________


#___________________________________________________________________________________________________________
#main function'
            
menu()
