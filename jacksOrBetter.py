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

# Load Images
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
selected_card_img = pygame.image.load(
    'graphics/buttons/selected_card_img.png').convert_alpha()
selected_card_img = pygame.transform.scale(
    selected_card_img, (int(selected_card_img.get_width() * 0.5), int(selected_card_img.get_height() * 0.5)))
# CLASSES:
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
        self.selected = False
        self.pressed = False

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

    def isSelected(self):
        return self.selected

    def unselect(self):
        self.selected = False

    def draw(self):
        # Get mouse pos
        # Check mouse over and clicked conditions
        if not game.getTurnState == 2:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.selected == False and not self.pressed:
                    self.selected = True
                    self.pressed = True
                    print('selected')
                if self.pressed:
                    if pygame.mouse.get_pressed()[0] == 0:
                        self.pressed = False

                if pygame.mouse.get_pressed()[0] == 1 and self.selected == True and not self.pressed:
                    self.selected = False
                    self.pressed = True
                    print('unselected')
                if self.pressed:
                    if pygame.mouse.get_pressed()[0] == 0:
                        self.pressed = False

        if (self.selected):
            screen.blit(self.image, (self.rect.x, self.rect.y))
            screen.blit(selected_card_img, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.selected
# GAME


class Game():
    def __init__(self):
        # Game Info
        self.new_game = True
        self.game_active = False
        self.turn_state = 0
        # Card Info
        self.cards_visible = False
        self.drawn_cards = []
        self.cards_displayed = []
        # Deck Info
        self.curr_deck = []
        # Draw Info
        self.cards_to_draw = 5

    def getFreshDeck(self):
        unshuffled_deck = []
        files = []
        for f in os.listdir('graphics/cards'):
            files.append(f)

        for i in files:
            arr = i.split('_')
            arr[-1] = arr[-1][:-4]
            unshuffled_deck.append(
                Card(arr[0], arr[1], arr[2], arr[3], pygame.image.load('graphics/cards/{}'.format(i)).convert_alpha(), .5))
        self.curr_deck = unshuffled_deck
        random.shuffle(self.curr_deck)

    def isActive(self):
        return self.game_active

    def setActive(self, bool):
        self.game_active = bool

    def isNewGame(self):
        return self.new_game

    def getTurnState(self):
        return self.turn_state

    def isCardsVisible(self):
        return self.cards_visible

    def getCurrDeck(self):
        return self.curr_deck

    def getDrawnCards(self):
        return self.drawn_cards

    def getDisplayedCards(self):
        return self.cards_displayed

    def setDisplayedCards(self, arr):
        self.cards_displayed = arr

    def setCardsVisible(self, bool):
        self.cards_visible = bool

    def getCardsToDraw(self):
        return self.cards_to_draw

    def setCardsToDraw(self, num):
        self.cards_to_draw = num

    def setTurnState(self, state):
        self.turn_state = state

    def setDrawnCards(self, arr):
        self.drawn_cards = arr

    def drawCard(self, i):
        next_card = self.curr_deck.pop(0)
        if len(self.drawn_cards) - 1 < i:
            self.drawn_cards.append(next_card)
        else:
            self.drawn_cards[i] = next_card
        print(len(self.drawn_cards))
        next_card.setPos(i)


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


# TIME
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


# Create Game
game = Game()

# GAME LOOP
while True:
    # EVENT LOOP
    for event in pygame.event.get():
        # quit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # GAME ACTIVE
        if game.isActive:
            ...

        # Display Cards

    if game.isActive():
        # SCREEN
        screen.blit(table_background_img, (0, 0))
        if game.isCardsVisible():
            for card in game.getDrawnCards():
                card.draw()
        print(game.getTurnState())
        if draw_button.draw():

            if game.getTurnState() == 2:
                # PAY OUT / RESET
                # DISPLAY PAYOUT
                for card in game.getDrawnCards():
                    card.unselect()
                game.setCardsVisible(False)
                game.setTurnState(0)

            elif game.getTurnState() == 1:
                # KEEP / DISCARD
                cards_to_discard = []
                index = 0
                for card in game.getDrawnCards():
                    if card.isSelected():
                        cards_to_discard.append([card, index])
                    card.unselect()
                    index += 1

                game.setCardsToDraw(len(cards_to_discard))
                for card in cards_to_discard:
                    game.drawCard(card[1])
                game.setTurnState(2)

            else:
                # TURN JUST STARTED
                game.getFreshDeck()
                print(game.getCardsToDraw())
                for i in range(0, game.getCardsToDraw()):
                    game.drawCard(i)
                game.setCardsVisible(True)
                game.setTurnState(1)

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

    else:
        # SCREEN
        screen.blit(start_background_img, (0, 0))
        if start_button.draw():
            print('Start')
            game.setTurnState(0)
            game.setActive(True)

        if settings_button.draw():
            print('Settings')

        if quit_button.draw():
            print('Quit')
            pygame.quit()
            exit()

    pos = pygame.mouse.get_pos()
    pygame.display.update()
    clock.tick(60)
