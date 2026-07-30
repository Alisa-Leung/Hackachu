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
firstCard = None
secondCard = None
locked = False
flipBackTime = 0
matches = 0
tries = 0
startTime = 0
elapsedTime = 0
currentCursor = pygame.SYSTEM_CURSOR_ARROW

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
cardBack = scaleImage(images["cardBack"], 4)
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
        self.isMatched = False
    def setFlipped(self, isFlipped):
        self.isFlipped = isFlipped

def createDeck():
    global deck
    deck = []
    for i in range(2):
        for key, value in images.items():
            if "card_" in key:
                card = Card(key.replace("card_", "",), scaleImage(value, 4))
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
    padding = 5
    cardBack = scaleImage(images["cardBack"], scale)
    cardWidth = cardBack.get_width()
    cardHeight = cardBack.get_height()
    totalWidth = 4 * cardWidth + 3 * padding
    totalHeight = 4 * cardHeight + 3 * padding
    startX = (gameWidth - totalWidth) // 2
    startY = (gameHeight - totalHeight) // 2
    for row in range(4):
        for column in range(4):
            x = startX + column * (cardWidth + padding) + 75
            y = startY + row * (cardHeight + padding)
            deck[row][column].rect = pygame.Rect(x, y, cardWidth, cardHeight)

def displayCards():
    global locked, currentCursor
    mousePos = pygame.mouse.get_pos()
    hovering = False
    for row in deck:
        for card in row:
            if card.isFlipped:
                image = card.image
            else:
                image = cardBack
            if card.rect.collidepoint(mousePos) and not locked and not card.isFlipped and not card.isMatched:
                hovering = True
                hoverRect = card.rect.move(0, -8)
                screen.blit(image, hoverRect)
            else:
                screen.blit(image, card.rect)
    newCursor = pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW
    if newCursor != currentCursor:
        pygame.mouse.set_cursor(newCursor)
        currentCursor = newCursor

def checkCards(card):
    global locked, flipBackTime, firstCard, secondCard, matches, tries
    if card.rect.collidepoint(event.pos) and not card.isFlipped and not card.isMatched:
        card.setFlipped(True)
        if firstCard is None:
            firstCard = card
        elif secondCard is None:
            secondCard = card
            tries += 1
            if firstCard.name == secondCard.name:
                firstCard.isMatched = True
                secondCard.isMatched = True
                matches += 1
                firstCard = None
                secondCard = None
            else:
                locked = True
                flipBackTime = pygame.time.get_ticks() + 1000
def resetGame():
    global firstCard, secondCard, locked, flipBackTime, matches, tries, startTime, elapsedTime
    firstCard = None
    secondCard = None
    locked = False
    flipBackTime = 0
    matches = 0
    tries = 0
    startTime = 0
    elapsedTime = 0

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
        "[Press SPACE to begin!]"
    ]
    for i, line in enumerate(introLines):
        introText = textFont.render(line, True, (47, 54, 153))
        introRect = introText.get_rect(center=(gameWidth//2, 100 + i * 100))
        screen.blit(introText, introRect)

def playScreen():
    global tries, elapsedTime
    screen.fill((112, 154, 209))
    displayCards()
    moveText = textFont.render("Moves: " + str(tries), True, (47, 54, 153))
    screen.blit(moveText, (10, 10))
    minutes = elapsedTime // 60
    seconds = elapsedTime % 60
    timerText = textFont.render(f"Time: {minutes}:{seconds:02}", True, (47, 54, 153))
    screen.blit(timerText, (10, 60))

def winScreen():
    global tries
    screen.fill((112, 154, 209))
    winLines = [
        "Congrats on winning the game!",
        "Tries: " + str(tries),
        "Time: " + str(elapsedTime) + "s",
        "[Press R to play again]"
    ]
    for i, line in enumerate(winLines):
        winText = textFont.render(line, True, (47, 54, 153))
        winRect = winText.get_rect(center=(gameWidth//2, 150 + i * 100))
        screen.blit(winText, winRect)

def draw():
    global elapsedTime
    match gameState:
        case "start":
            startScreen()
        case "intro":
            introScreen()
        case "play":
            playScreen()
            elapsedTime = (pygame.time.get_ticks() - startTime) // 1000
        case "win":
            winScreen()

while isPlaying:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == "start":
                if playRect.collidepoint(mousePos):
                    playPressed = True
            if gameState == "play" and not locked:
                for row in deck:
                    for card in row:
                        checkCards(card)
        if event.type == pygame.MOUSEBUTTONUP:
            if gameState == "start" and playPressed:
                if playRect.collidepoint(mousePos):
                    playPressed = False
                    gameState = "intro"
        if event.type == pygame.KEYDOWN:
            if gameState == "intro" and event.key == pygame.K_SPACE:
                resetGame()
                createDeck()
                startTime = pygame.time.get_ticks()
                gameState = "play"
            if gameState == "win" and event.key == pygame.K_r:
                resetGame()
                createDeck()
                gameState = "play"
    if locked and pygame.time.get_ticks() >= flipBackTime:
        firstCard.setFlipped(False)
        secondCard.setFlipped(False)
        firstCard = None
        secondCard = None
        locked = False
    if matches == 8 and firstCard is None and secondCard is None:
        gameState = "win"
    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()