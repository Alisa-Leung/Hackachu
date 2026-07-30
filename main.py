import pygame
import sys
import os
import random

pygame.init()

gameWidth = 800
gameHeight = 600

screen = pygame.display.set_mode([gameWidth, gameHeight])
isPlaying = True
gameState = "start"
playPressed = False

icon = pygame.image.load('assets/cardBack.png')
pygame.display.set_icon(icon)

def loadImages():
    images = {}
    for fileName in os.listdir("assets/"):
        if fileName.endswith('.png'):
            path = os.path.join("assets/", fileName)
            image = pygame.image.load(path).convert_alpha()
            key = os.path.splitext(fileName)[0]
            images[key] = image
    return images

def scaleImage(image, mult):
    return pygame.transform.scale_by(image, mult)

images = loadImages()
playRect = scaleImage(images['buttonUnpressed'], 3).get_rect(center=(gameWidth//2, gameHeight//2))
titleFont = pygame.font.Font("assets/pixelify.ttf", 70)
textFont = pygame.font.Font("assets/pixelify.ttf", 30)

bgY1 = 0
bgY2 = -gameHeight

def scrollBackground():
    bgSpeed = 0.125
    global bgY1, bgY2
    bg = pygame.transform.scale(images['background'], (gameWidth, gameHeight))
    screen.blit(bg, (0, bgY1))
    screen.blit(bg, (0, bgY2))
    bgY1 += bgSpeed
    bgY2 += bgSpeed
    if bgY1 >= gameHeight:
        bgY1 = -gameHeight
    if bgY2 >= gameHeight:
        bgY2 = -gameHeight

class Card:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.rect = None  
        self.isFlipped = False
    def setFlipped(self, isFlipped):
        self.isFlipped = isFlipped

def createDeck():
    global deck
    deck = []
    for i in range(2):
        for key, value in images.items():
            if "card_" in key:
                card = Card(key.replace("card_", "",), value)
                deck.append(card)
    random.shuffle(deck)
    deckTable = []
    cardIndex = 0
    for row in range(4):
        deckRow = []
        for column in range(4):
            deckRow.append(deck[cardIndex])
            cardIndex += 1
        deckTable.append(deckRow)
    deck = deckTable
    scale = 4
    padding = 25
    cardBack = scaleImage(images["cardBack"], scale)
    cardWidth = cardBack.get_width()
    cardHeight = cardBack.get_height()
    totalWidth = 4 * cardWidth + 3 * padding
    totalHeight = 4 * cardHeight + 3 * padding
    startX = (gameWidth - totalWidth) // 2
    startY = (gameHeight - totalHeight) // 2
    for row in range(4):
        for column in range(4):
            x = startX + column * (cardWidth + padding)
            y = startY + row * (cardHeight + padding)
            deck[row][column].rect = pygame.Rect(x, y, cardWidth, cardHeight)

def displayCards():
    scale = 4
    for row in deck:
        for card in row:
            if card.isFlipped:
                image = scaleImage(card.image, scale)
            else:
                image = scaleImage(images["cardBack"], scale)
            screen.blit(image, card.rect)

def startScreen():
    scrollBackground()
    currentButton = scaleImage((images['buttonPressed'] if playPressed else images['buttonUnpressed']), 3)
    screen.blit(currentButton, playRect)

def introScreen():
    screen.fill((112, 154, 209))
    introLines = [
        "Welcome to my game!",
        "Let's test your memory.",
        "Find the matching cards",
        "with the least tries possible!",
        "Click anywhere to begin!"
    ]
    for i, line in enumerate(introLines):
        introText = textFont.render(line, True, (47, 54, 153))
        introRect = introText.get_rect(center=(gameWidth//2, 100 + i * 100))
        screen.blit(introText, introRect)

def playScreen():
    screen.fill((112, 154, 209))
    displayCards()

def draw():
    match gameState:
        case "start":
            startScreen()
        case "intro":
            introScreen()
        case "play":
            playScreen()

while isPlaying:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == "start":
                if playRect.collidepoint(mousePos):
                    playPressed = True
            if gameState == "intro":
                createDeck()
                gameState = "play"
            if gameState == "play":
                for row in deck:
                    for card in row:
                        if card.rect.collidepoint(event.pos):
                            card.setFlipped(True)
        if event.type == pygame.MOUSEBUTTONUP:
            if gameState == "start" and playPressed:
                if playRect.collidepoint(mousePos):
                    playPressed = False
                    gameState = "intro"
    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()

# game loop

# initial bet
# 3 cards dealt are dealt to each person
# players look at cards
# 2nd bet
# 

# game loop
# pay initial amt
# 3 cards dealt
# cards in middle face down
# initial bet
# show one card

# percentages
# 15 cards total
# to do: 2 hits
# 2 cool cards --> full art items
# 6 item cards 
# to do: 1 energy card --> but then u gotta do all of em