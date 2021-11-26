from math import floor
import sys

import pygame
import random

from pygame.mixer import Sound

pygame.init()
SCREENWIDTH, SCREENHEIGHT  = 1280, 720
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
buttonImage = pygame.image.load("media/logo.png").convert_alpha()
meteorImg = pygame.image.load("media/meteor.png").convert_alpha()
playerImg = pygame.image.load("media/player.png").convert_alpha()
playerImg = pygame.transform.scale2x(playerImg)

pygame.display.set_caption("One Button")
pygame.display.set_icon(buttonImage)
font = pygame.font.SysFont("Arial", 30)
pygame.mixer.init()

#jsfxr was used for sounds
#https://sfxr.me/
explosion = pygame.mixer.Sound("media/explosion.wav")
explosion.set_volume(0.2)
whoosh = pygame.mixer.Sound("media/whoosh.wav")
whoosh.set_volume(0.2)
bling = pygame.mixer.Sound("media/bling.wav")
bling.set_volume(0.2)

class data:
    cachedElements = []
    screens = ["mainScreen", "level1", "level2"]
    playerData = [SCREENWIDTH/2, SCREENHEIGHT-50, True, True]
    meteorData = []
    endGame = False
    difficulty = 3
    score = 0

class main:

    def tick():
        #define variables/code that executes on start
        #cachedElements.append([buttonImage, (1000, 500), "Image at 1000, 500"])
        data.cachedElements.append([(200, 20, 20), (0, SCREENHEIGHT-40,SCREENWIDTH ,SCREENHEIGHT), "Rect at 20, 20"])
        data.score = 1
        difficulty = 2
        #loop
        while True:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

            if data.endGame:
                return
            data.score += 1
            if data.score %1000 == 0:
                data.playerData[2] = not data.playerData[2]
                data.difficulty += 1
                bling.play()
            screen.fill((20, 20, 20 ))
            if data.playerData[0] > 10 and data.playerData[2]:
                data.playerData[0] -= 10
            elif data.playerData[0] < SCREENWIDTH -20 and not data.playerData[2]:
                data.playerData[0] += 10
            if pygame.key.get_pressed()[pygame.K_SPACE] == True or pygame.mouse.get_pressed()[0] == True:
                main.spaceClicked()
            main.drawCachedElements()
            main.meteorTick()
            screen.blit(playerImg, (data.playerData[0], data.playerData[1]))
            screen.blit(menu.generateTextObject(str(floor(data.score)), (255, 255, 255), 100), (20, 20))
            pygame.display.update()
    
    
    def spaceClicked():
        '''when space or the screen is clicked\n 
        space clicks multiple times per second'''
        if data.playerData[0] < SCREENWIDTH-30 and data.playerData[2]:
            data.playerData[0] += 20
        elif data.playerData[0] > 10 and not data.playerData[2]:
            data.playerData[0] -= 20
        return

    def meteor():
        if len(data.meteorData) < data.difficulty:
            speed = random.randint(1, 5)
            data.meteorData.append([random.randint(0, SCREENWIDTH-100), 0, 2*speed])
            whoosh.play()
    def meteorTick():
        iteration = -1
        if random.random() < 0.1:
            main.meteor()
        for meteor in data.meteorData:
            iteration += 1
            meteor[1] += meteor[2]
            if pygame.Rect(meteor[0], meteor[1], 100, 100).colliderect(data.playerData[0], data.playerData[1], 30, 80):
                data.meteorData.pop(iteration)
                endGame = True
                raise Exception
            elif meteor[1] > SCREENHEIGHT-50:
                data.meteorData.pop(iteration)
                explosion.play()
            else:
                screen.blit(meteorImg, (meteor[0], meteor[1]))

    def drawCachedElements():
        '''re-draws all cached elements'''
        for element in data.cachedElements:
            if "Rect" in element[2]:
                pygame.draw.rect(screen, element[0], element[1])
            elif "Image" or "Text" in element[2]:
                screen.blit( element[0], element[1])


    def deleteCachedElement(tag):
        for element in data.cachedElements:
            if element[2] == tag:
                data.cachedElements.remove(element)

    def removeAllCache():
        data.cachedElements = []
        data.playerData = [SCREENWIDTH/2, SCREENHEIGHT-50, True, True]
        data.meteorData = []
class menu:
    def __init__() -> None:
        pass
    
    def registerScreenImage(xpos, ypos, image) -> None:
        screen.blit(pygame.image.load(image).convert_alpha, (xpos, ypos))

    def generateTextObject(text = "undifined", colour = (0, 0, 0), size = 30):
        return pygame.font.SysFont("Arial", size).render(text, False, colour)
    def waitLoopThing():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                pygame.key.set_repeat(0, 0)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

if __name__ == "__main__":
    while True:
        try:
            main.tick()
        except Exception:
            pass
        prevScore = data.score
        main.removeAllCache()
        pygame.mixer.stop()
        screen.fill((20, 20, 20))
        screen.blit(menu.generateTextObject("Play Again?",(255, 255, 255)), (SCREENWIDTH/2-100, SCREENHEIGHT/2))
        screen.blit(menu.generateTextObject("Previous score: " + str(prevScore),(200, 200, 200)), (SCREENWIDTH/2-100, SCREENHEIGHT/2+100))
        data.cachedElements = []
        data.playerData = [SCREENWIDTH/2, SCREENHEIGHT-50, True, True]
        data.meteorData = []
        data.difficulty = 3
        pygame.display.update()
        menu.waitLoopThing()