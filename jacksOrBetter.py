import os.path
import os
from PIL import Image
from math import trunc
import pygame
from sys import exit
import random


pygame.init()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption('Jacks or Better')
clock = pygame.time.Clock()
casino_font = pygame.font.Font('font/Casino.ttf', 50)
game_active = False
new_game = True
cards_to_draw = 5
ready_to_draw = False
turn_state = 0
drawn_cards = []
displaying_cards = []
card_buttons = []
view_cards = False

# # Load Images
# Start Screen
start_background_img = pygame.image.load(
    'graphics/start_background.png').convert_alpha()
# Background of Game Screen
table_background_img = pygame.image.load(
    'graphics/table_background.png').convert_alpha()

# Buttons
start_button_img = pygame.image.load(
    'graphics/buttons/start_button.png').convert_alpha()
settings_button_img = pygame.image.load(
    'graphics/buttons/settings_button.png').convert_alpha()
see_pays_button_img = pygame.image.load(
    'graphics/buttons/see_pays_button.png').convert_alpha()
speed_button_img = pygame.image.load(
    'graphics/buttons/speed_button.png').convert_alpha()
draw_button_img = pygame.image.load(
    'graphics/buttons/draw_button.png').convert_alpha()
quit_button_img = pygame.image.load(
    'graphics/buttons/quit_button.png').convert_alpha()
options_button_img = pygame.image.load(
    'graphics/buttons/options_button.png').convert_alpha()
blank_button_img = pygame.image.load(
    'graphics/buttons/blank_button.png').convert_alpha()
back_button_img = pygame.image.load(
    'graphics/buttons/back_button.png').convert_alpha()

# CARD


class Card():
    def __init__(self, id, value, suit, color, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))

        self.value = value
        self.id = id
        self.suit = suit
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.clicked = False

    def setPos(self, num):
        # Set card position when drawn
        print('pos set')
        if num == 0:
            self.rect.topleft = (5, 430)
        elif num == 1:
            self.rect.topleft = (260, 430)
        elif num == 2:
            self.rect.topleft = (515, 430)
        elif num == 3:
            self.rect.topleft = (770, 430)
        else:
            self.rect.topleft = (1025, 430)

    def getPos(self):
        return self.rect.topleft

    def getImage(self):
        return self.image

    def draw(self):
        action = False
        # Get mouse pos
        pos = pygame.mouse.get_pos()
        # Check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Get card-file names
files = []
valid_images = [".jpg", ".gif", ".png", ".tga"]
for f in os.listdir('graphics/cards'):
    ext = os.path.splitext(f)[1]
    files.append(f)

# Get Unshuffled Deck


def getUnshuffledDeck():
    unshuffled_deck = []
    for i in files:
        arr = i.split('_')
        arr[-1] = arr[-1][:-4]
        unshuffled_deck.append(
            Card(arr[0], arr[1], arr[2], arr[3], pygame.image.load('graphics/cards/{}'.format(f)).convert_alpha(), .5))
    return unshuffled_deck


# Get Base Deck
base_deck = getUnshuffledDeck()

# Shuffle Deck


def shuffleDeck(deck):
    arr_copy = list(deck)
    random.shuffle(arr_copy)
    return arr_copy

# BUTTON


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # Get mouse pos
        pos = pygame.mouse.get_pos()
        # Check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Create button instances
# Start screen buttons
start_button = Button(100, 700, start_button_img, 1)
settings_button = Button(500, 700, settings_button_img, 1)
quit_button = Button(900, 700, quit_button_img, 1)
# Game screen buttons
see_pays_button = Button(5, 850, see_pays_button_img, 1)
options_button = Button(325, 850, options_button_img, 1)
blank_button = Button(645, 850, blank_button_img, 1)
draw_button = Button(965, 850, draw_button_img, 1)
back_button = Button(5, 920, back_button_img, .5)
# see_pays_button = Button(5, 850, see_pays_button_img)


# TIME
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# GAME LOOP
while True:
    # EVENT LOOP
    for event in pygame.event.get():
        # quit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # GAME ACTIVE
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_gravity = -20

    if game_active:
        # SCREEN
        screen.blit(table_background_img, (0, 0))
        if view_cards:
            displaying_cards[0].draw()
            displaying_cards[1].draw()
            displaying_cards[2].draw()
            displaying_cards[3].draw()
            displaying_cards[4].draw()

        if draw_button.draw():

            if turn_state == 0:  # TURN JUST STARTED
                print(turn_state)
                # Get Shuffled Deck
                shuffledDeck = shuffleDeck(base_deck)
                print(shuffledDeck)
                # DRAW 5
                for i in range(0, cards_to_draw):
                    drawn_cards.append(shuffledDeck[i])
                    drawn_cards[i].setPos(i)
                displaying_cards = drawn_cards
                drawn_cards = []
                view_cards = True

                # turn_state += 1

            # if turn_state == 1:  # KEEP / DISCARD CARDS
            #     print(turn_state)
            #     turn_state += 1
            #     # DRAW WHAT IS NEEDED
            #     continue

            # if turn_state == 2:  # PAYOUT
            #     print(turn_state)
            #     # RESET
            #     turn_state = 0
            #     continue

            # TODO: DRAW
        blank_button.draw()
        if see_pays_button.draw():
            ...
            # TODO: SEE PAYS SCREEN

        if options_button.draw():
            ...
            # TODO: OPTIONS SCREEN

        if back_button.draw():
            game_active = False
            # TODO: DRAW

        # TODO Shuffle
        # TODO Deal
        # TODO Allow Keep / Discard
        # TODO DRAW
        # TODO Payout
        # TODO Repeat

    else:
        # SCREEN
        screen.blit(start_background_img, (0, 0))
        if start_button.draw():
            print('Start')
            turn_state = 0
            game_active = True

        if settings_button.draw():
            print('Settings')

        if quit_button.draw():
            print('Quit')
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
