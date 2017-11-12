#15-112: Fundementals of Programming and Computer Science
#Final Project
#Name: Andrew Edward
#AndrewID: aedward

import pygame
from pygame.locals import *
import Tkinter
from PIL import ImageTk, Image
import sys    
      
        
#MAIN MENU WINDOW
def Menu():
    
    root = Tkinter.Tk()
    root.geometry("1024x768")

    #get background image and place it
    Background = ImageTk.PhotoImage(Image.open("Images/galaxy3.png"))
    BackgroundLabel = Tkinter.Label(root, image = Background)
    BackgroundLabel.place(x=0,y=0,relwidth=1,relheight=1)

    #Buttons, and they labels
    play_Btn_Image = ImageTk.PhotoImage(Image.open("Images/play2.png"))
    how_Btn_Image = ImageTk.PhotoImage(Image.open("Images/how2.png"))
    playBtn = Tkinter.Button(root, image = play_Btn_Image, borderwidth=0, command=lambda x=root:play(x))
    howBtn = Tkinter.Button(root, image = how_Btn_Image, borderwidth=0, command=lambda x=root:how(x))

    #pack buttons
    playBtn.pack(pady=(300,5))
    howBtn.pack(pady=50)

    root.mainloop()

#HOW TO PLAY WINDOW
def how(close):
    #close the main menu
    close.destroy()
    #load the new window
    root = Tkinter.Tk()
    root.geometry("1024x768")

    #get background image and place it
    Background = ImageTk.PhotoImage(Image.open("Images/galaxy1.png"))
    BackgroundLabel = Tkinter.Label(root, image = Background)
    BackgroundLabel.place(x=0,y=0,relwidth=1,relheight=1)

    #place the instructions image
    HOW_TO_PLAY = Image.open("Images/howtoplay.png")
    HOW_TO_PLAY = HOW_TO_PLAY.resize((900,600))
    HOW_TO_PLAY = ImageTk.PhotoImage(HOW_TO_PLAY)
    HOW_TO_PLAYLabel = Tkinter.Label(root, image = HOW_TO_PLAY , borderwidth=0, width = 900, height = 600)
    HOW_TO_PLAYLabel.photo = HOW_TO_PLAY
    
    Back_Btn_Image = ImageTk.PhotoImage(Image.open("Images/back.png"))
    BackBtn = Tkinter.Button(root, image =Back_Btn_Image, borderwidth=0, command=lambda x=root:getback(x))

    #pack instructions label
    HOW_TO_PLAYLabel.pack(pady=(20,5))
    BackBtn.pack(pady=(40,0))
    
    root.mainloop()

#function to re-create a menu when "back" button is clicked
def getback(x):
    x.destroy()
    Menu()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        #save to images for the spaceship, one when it's not moving, other when a button is clicked
        self.static = pygame.image.load("Images/sprite static.png").convert_alpha()
        self.moving = pygame.image.load("Images/sprite right.png").convert_alpha()
        self.image = self.static
        self.rect = self.image.get_rect()
        #for location of image
        self.rect.x = x
        self.rect.y = y
        self.surface = screen
        #amount of points the spaceship moves
        self.dist=15
        self.frame=0
        
    def movements(self):

        #if the D key is pressed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.image=self.moving
            #to be sure the spaceship is always inside the window
            if self.rect.x<920:
                self.rect.x = self.rect.x + self.dist

        #if the A key is pressed
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            #flips the image (((1)))
            self.image=pygame.transform.flip(self.moving,1,0)
            #to be sure the spaceship is always inside the window
            if self.rect.x!=0:
                self.rect.x = self.rect.x - self.dist   
        #if no key is pressed
        elif pygame.event.get()==[]:
            self.image=self.static

    #draws the object on the screen
    def draw(self,surface):
        self.surface.blit(self.image, self.rect)


class Laser(pygame.sprite.Sprite): #I know it's a rocket but until I find a good quality laser picture
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)

        #load the picture of the laser
        self.image = pygame.image.load("Images/laser1.png").convert_alpha()
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


class birds(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        #load the picture of bird
        self.image = pygame.image.load("Images/bird2.png").convert_alpha()
        self.rect = self.image.get_rect()
        #for location of bird
        self.rect.x = x
        self.rect.y = y
        self.surface = screen
        self.dead = False

    #draws the object on screen
    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        if self.dead == True:
            self.rect.x = -1
            self.rect.y = -1

#MAIN GAME WINDOW

def play(close):
    #close the main menu
    close.destroy()

    #call pygame
    pygame.init()
    
    #Constants
    FPS=60
    WHITE = (255, 255, 255)
    OFF = 0
    LIVE = 0
    status = LIVE
    current_Score = 0
    cSText = pygame.font.SysFont('Arial',20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))

    #for FPS
    clock = pygame.time.Clock()

    #elements of game
    screen = pygame.display.set_mode((1024,768),0,32)
    pygame.display.set_caption('Kill the birds')
    background=pygame.image.load("Images/galaxy1.png")
    screen.fill(WHITE)
    player=Spaceship(screen,450,600)
    BIRD = birds(screen,450,50)
    lasers_list = []
    birds_list = [BIRD]

    #starting:
    
    screen.blit(background,(0,0))
    screen.blit(cSText,(0,0))
    player.draw(screen)
    BIRD.draw()
    pygame.display.update()


    pygame.time.delay(2000)

    
    while True:
        for event in pygame.event.get():
            #if statement to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if a space is clicked, it begins firing laser
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if lasers_list == []:
                    laser = Laser(screen, player.rect.x+5,player.rect.y)
                    lasers_list = lasers_list + [laser]
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

            #update interface            
            screen.blit(background,(0,0))
            screen.blit(cSText,(0,0))
            player.draw(screen)

            #initialize birds
            for i in birds_list:
                i.draw()
            #initialize laser
            for i in lasers_list:
                i.draw()
            #check for coallition
            for i in lasers_list:
                if pygame.sprite.collide_rect(BIRD,i):
                    #make the condition true so you can remove the object
                    BIRD.dead = True
                    BIRD.update()
                    lasers_list.remove(i)
                    birds_list = []
                    current_Score = current_Score + 1
            #if game is not over, keep updating
            if OFF != 1:
                cSText =pygame.font.SysFont('Arial', 20).render(('Current Score: '+str(current_Score)), True, pygame.color.Color('White'))
                screen.blit(cSText,(0,0))

            pygame.display.flip()
            clock.tick(60)

#main function'
Menu()
