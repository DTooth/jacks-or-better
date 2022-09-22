from ast import Num
import os.path
import os
from PIL import Image
from math import trunc
import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode(
    (1280, 960), flags=pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('Jacks or Better')
clock = pygame.time.Clock()
casino_font = pygame.font.Font('font/casino_font.ttf', 50)
casino_font_small = pygame.font.Font('font/casino_font.ttf', 35)
instruction_font = pygame.font.Font('font/raleway.ttf', 25)

# Load Images
# Start Screen
start_background_img = pygame.image.load(
    'graphics/start_background.png').convert_alpha()
# Background of Game Screen
table_background_img = pygame.image.load(
    'graphics/table_background.png').convert_alpha()
table_background_highlight_img = pygame.image.load(
    'graphics/table_background_highlight.png').convert_alpha()
table_background_highlight_rect = table_background_highlight_img.get_rect()

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
    # Card

    def getCardValue(self):
        return self.value

    def getCardSuit(self):
        return self.suit

    def getCardColor(self):
        return self.color

    def setPos(self, num):
        # Set card position when drawn
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
        if not game.getTurnState() == 2:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.selected == False and not self.pressed:
                    self.selected = True
                    self.pressed = True
                    # print('selected')
                if self.pressed:
                    if pygame.mouse.get_pressed()[0] == 0:
                        self.pressed = False

                if pygame.mouse.get_pressed()[0] == 1 and self.selected == True and not self.pressed:
                    self.selected = False
                    self.pressed = True
                    # print('unselected')
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
        # Payout Structure:
        self.payout = [250, 50, 25, 9, 6, 4, 3, 2, 1]
        self.payout_key = ['Royal Flush', 'Straight Flush', '4 of a Kind', 'Full House',
                           'Flush', 'Straight', '3 of a Kind', '2 Pair', 'Jacks or Better']
        # Game Info
        self.isWin = False
        self.yellow = (255, 200, 0)
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
        # Credit / Bet Info
        self.credit = 100
        self.bet = 1
        # Credit / bet Text
        self.bet_text = casino_font.render(
            'BET: {}'.format(self.bet), True, self.yellow)
        self.bet_text_rect = self.bet_text.get_rect()
        self.bet_text_rect.center = (785, 882)

        self.credit_text = casino_font_small.render(
            'CREDITS: {}'.format(self.credit), True, (255, 255, 250)
        )
        self.credit_text_rect = self.credit_text.get_rect()
        self.credit_text_rect.topleft = (675, 920)

        self.instruc_text = None
        self.instruc_text_rect = None

    def getPayoutName(self, index):
        return self.payout_key[index]

    def setInstrucText(self, text):
        self.instruc_text = instruction_font.render(
            text, True, (255, 255, 250))
        self.instruc_text_rect = self.instruc_text.get_rect()
        self.instruc_text_rect.topleft = (5, 400)

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

    def getCredits(self):
        return self.credit

    def subtractCredits(self, num):
        if (num > self.credit):
            return False
        self.credit = self.credit - num
        self.credit_text = casino_font_small.render(
            'CREDITS: {}'.format(self.credit), True, (255, 255, 250)
        )
        return True

    def addCredits(self, num):
        # print('{} credits have been added!'.format(num))
        self.credit = self.credit + num
        self.credit_text = casino_font_small.render(
            'CREDITS: {}'.format(self.credit), True, (255, 255, 250)
        )

    def isWin(self):
        return self.isWin

    def setIsWin(self, bool):
        self.isWin = bool

    def getBet(self):
        return self.bet

    def increaseBet(self):
        if self.bet == 5:
            self.bet = 1
        else:
            self.bet += 1
        self.bet_text = casino_font.render(
            'BET: {}'.format(self.getBet()), True, self.yellow)

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
        # print(len(self.drawn_cards))
        next_card.setPos(i)

    def checkPayout(self, cards):
        valueMap = {}
        suitMap = {}
        for card in cards:
            # print(card.getCardValue())
            # print(card.getCardSuit())
            if card.getCardSuit in suitMap.keys():
                suitMap[card.getCardSuit()] = suitMap[card.getCardSuit()] + 1
            else:
                suitMap[card.getCardSuit()] = 1

            if card.getCardValue() in valueMap.keys():
                valueMap[card.getCardValue()] = valueMap[card.getCardValue()] + 1
            else:
                valueMap[card.getCardValue()] = 1

        # TODO: Check payout for given hand
        self.payout_level = 0
        # Check Royal Flush:
        if len(suitMap) == 1:
            # print('FLUSH')
            if (len(valueMap.keys()) > 0):
                # print(list(valueMap.keys()))
                card_values = []
                for num in list(valueMap.keys()):
                    card_values.append(int(num))
                card_values.sort()
                if (card_values[0] == 10):
                    # print('ROYAL FLUSHHH')
                    if (self.bet == 5):
                        return 4000
                    return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Straight Flush:
        if len(valueMap) == 5:
            if (len(valueMap.keys()) > 0):
                # print(list(valueMap.keys()))
                card_values = []
                for num in list(valueMap.keys()):
                    card_values.append(int(num))
                card_values.sort()
                start = card_values[0]
                # print(card_values)
                early_break = False
                for val in card_values:
                    if not start == val:
                        early_break = True
                        break
                    start += 1
                if not early_break and len(suitMap) == 1:
                    # print('STRAIGHT - FLUSH !!!!!!!!!!!!!')
                    return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Four of a Kind:
        if len(valueMap.keys()) == 2:
            if list(valueMap.values()).sort() == [1, 4]:
                # print('Four of a Kind!!')
                return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Full House
        if len(valueMap.keys()) == 2:
            if list(valueMap.values()).sort() == [2, 3]:
                # print('Full House!')
                return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Flush
        if len(suitMap) == 1:
            # print('FLUSH')
            return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Straight
        if len(valueMap) == 5:
            if (len(valueMap.keys()) > 0):
                # print(list(valueMap.keys()))
                card_values = []
                for num in list(valueMap.keys()):
                    card_values.append(int(num))
                card_values.sort()
                start = card_values[0]
                # print(card_values)
                early_break = False
                for val in card_values:
                    if not start == val:
                        early_break = True
                        break
                    start += 1
                if not early_break:
                    # print("STRAIGHTTTTTTTT")
                    return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Three of a Kind
        for key in valueMap:
          # print('key', key, map[key])
            if valueMap[key] == 3:
                # print('Three of a Kind!')
                return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Two Pair
        if len(valueMap.keys()) == 3:
            # print('Two Pair!!!')
            return self.bet * self.payout[self.payout_level]

        self.payout_level += 1
        # Check Jacks or Better
        for key in valueMap:
          # print('key', key, map[key])
            if int(key) >= 11 and valueMap[key] == 2:
                # print('Jacks or Better')
                return self.bet * self.payout[self.payout_level]
        # No Pay
        return 0
    # TODO: Return amount to add. bet * payout


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

        # print(game.getTurnState())
        if game.getTurnState() == 0:
            game.setInstrucText(
                'Select BET to change bet. Select DRAW to place bet and draw cards.')
            screen.blit(game.instruc_text, game.instruc_text_rect)
        if game.getTurnState() == 1:
            game.setInstrucText(
                'Select cards to hold. Select DRAW to redraw unselected cards.')
            screen.blit(game.instruc_text, game.instruc_text_rect)
        if game.getTurnState() == 2:
            if game.isWin:
                game.setInstrucText(
                    'Congrats you have won {} credits on a {}! Select DRAW to play again.'.format(game.bet * game.payout[game.payout_level], game.getPayoutName(game.payout_level)))
            else:
                game.setInstrucText(
                    'Better luck next time. Selected DRAW to play again.')
            screen.blit(game.instruc_text, game.instruc_text_rect)

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
                    if not card.isSelected():
                        cards_to_discard.append([card, index])
                    card.unselect()
                    index += 1
                game.setCardsToDraw(len(cards_to_discard))
                for card in cards_to_discard:
                    game.drawCard(card[1])

                # CHECK PAYOUT FOR CURRENT drawn_cards

                payout = game.checkPayout(game.getDrawnCards())
                if payout > 0:
                    game.setIsWin(True)
                else:
                    game.setIsWin(False)

                game.addCredits(payout)

                game.setTurnState(2)

            else:
                # TURN JUST STARTED
                if game.subtractCredits(game.getBet()):
                    for card in game.getDrawnCards():
                        card.unselect()
                    game.getFreshDeck()
                    game.setDrawnCards([])
                    game.setCardsToDraw(5)
                    # print(game.getCardsToDraw())
                    for i in range(0, game.getCardsToDraw()):
                        game.drawCard(i)
                    game.setCardsVisible(True)

                    game.setTurnState(1)
                else:
                    if game.getCredits() == 0:
                        # print('Out of Credits')
                        ...

        if see_pays_button.draw():
            ...
            # TODO: SEE PAYS SCREEN

        if options_button.draw():
            ...
            # TODO: OPTIONS SCREEN

        if not game.getTurnState() == 1:
            if back_button.draw():
                game.setActive(False)
                game.setCardsVisible(False)
                game.setTurnState(0)
                # TODO: DRAW

        if blank_button.draw():
            if not game.getTurnState() == 1:
                game.increaseBet()

        screen.blit(game.bet_text, game.bet_text_rect)
        # BET UI INFO
        if game.getBet() == 1:
            screen.blit(table_background_highlight_img,
                        (290, 12))
        elif game.getBet() == 2:
            screen.blit(table_background_highlight_img,
                        (480, 12))
        elif game.getBet() == 3:
            screen.blit(table_background_highlight_img,
                        (670, 12))
        elif game.getBet() == 4:
            screen.blit(table_background_highlight_img,
                        (867, 12))
        else:
            screen.blit(table_background_highlight_img,
                        (1065, 12))
        screen.blit(game.credit_text, game.credit_text_rect)
    else:
        # SCREEN
        screen.blit(start_background_img, (0, 0))
        if start_button.draw():
            # print('Start')
            game.setTurnState(0)
            game.setActive(True)

        if settings_button.draw():
            # print('Settings')
            ...

        if quit_button.draw():
            # print('Quit')
            pygame.quit()
            exit()

    pos = pygame.mouse.get_pos()
    pygame.display.update()
    clock.tick(60)
