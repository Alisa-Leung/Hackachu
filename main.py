import pygame
import sys

pygame.init()

screen = pygame.display.set_mode([800, 600])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
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
# 