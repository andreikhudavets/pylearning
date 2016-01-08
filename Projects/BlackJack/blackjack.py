'''
Ask player how moch money he wants to spend
Give 2 cards to player
Give 2 cards to dealer, but show 1
Player can do one of the following
    Hit to receive another card(then dealer will continue)
        Player can bust and loose in this case
        Or he can receive a blackjack and wins 1.5 of initial bet
    Stand to stand with current hand total
    Pay insurance if dealer has an A
    Choose cost of A (1 or 11)
    Split if there are two same cards - bet be added to this hand (each hand will receive another card)
Double Down double your bet and receive one an only one new card. Can be allowed for certain total (9-11)
Dealer draw hands until he has 17 or higher and then he does not allowed to draw more cards
Possible results
    Dealer Wins (bet goes to the bank)
    Player Wins (get original bet)
    Push (bet is returned)
    If no more money in bank - game over
'''
'''
TEST CASES
    Hit
    BlackJack
    
'''
#---------------COMMANDS THAT CAN BE RUN DURING THE GAME---------------------------------------
class Command(object):
    """
    Abstract class
    activation_str  - must return key user need to press in order to activate this command
    description - must return string describing effect of this operation
    """
    def __str__(self):
        return self.activation_str + ": " + self.description
    def __repr__(self):
        return self.__str__()
        
class CommandExit(Command):
    def __init__(self):
        self.activation_str = "e"
        self.description = "exit game"

class CommandNewGame(Command):
    def __init__(self):
        self.activation_str = "n"
        self.description = "new game"

class CommandContinue(Command):
    def __init__(self):
        self.activation_str = ""
        self.description = "<Enter> next round"

class CommandHit(Command):
    def __init__(self):
        self.activation_str = "h"
        self.description = "hit - one more card"

class CommandStand(Command):
    def __init__(self):
        self.activation_str = "s"
        self.description = "stand - no more cards"
        
class CommandInsurance(Command):
    def __init__(self):
        self.activation_str = "i"
        self.description = "pay insurance"

class CommandChangeACost(Command):
    def __init__(self):
        self.activation_str = "a"
        self.description = "change cost of A"

class CommandSplit(Command):
    def __init__(self):
        self.activation_str = "p"
        self.description = "split hands"

class CommandDoubleDown(Command):
    def __init__(self):
        self.activation_str = "d"
        self.description = "double down"

class CommandProceed(Command):
    def __init__(self):
        self.activation_str = "j"
        self.description = "just continue"

#------------------------------EXCEPTIONS-----------------------------------------------------
class InvalidInput(Exception):
    pass

class DeckIsEmpty(Exception):
    pass

#----------------------------CLASS DECK------------------------------------------------------
import random
class Deck(object):
    downcard = 'XX'
    def __init__(self):
        self.cards = [(u'\u2660','A',11),(u'\u2660','2',2),(u'\u2660','3',3),(u'\u2660','4',4),(u'\u2660','5',5),(u'\u2660','6',6),(u'\u2660','7',7),(u'\u2660','8',8),(u'\u2660','9',9),(u'\u2660','10',10),(u'\u2660','J',10),(u'\u2660','Q',10),(u'\u2660','K',10),
                      (u'\u2665','A',11),(u'\u2665','2',2),(u'\u2665','3',3),(u'\u2665','4',4),(u'\u2665','5',5),(u'\u2665','6',6),(u'\u2665','7',7),(u'\u2665','8',8),(u'\u2665','9',9),(u'\u2660','10',10),(u'\u2665','J',10),(u'\u2665','Q',10),(u'\u2665','K',10),
                      (u'\u2666','A',11),(u'\u2666','2',2),(u'\u2666','3',3),(u'\u2666','4',4),(u'\u2666','5',5),(u'\u2666','6',6),(u'\u2666','7',7),(u'\u2666','8',8),(u'\u2666','9',9),(u'\u2660','10',10),(u'\u2666','J',10),(u'\u2666','Q',10),(u'\u2666','K',10),
                      (u'\u2663','A',11),(u'\u2663','2',2),(u'\u2663','3',3),(u'\u2663','4',4),(u'\u2663','5',5),(u'\u2663','6',6),(u'\u2663','7',7),(u'\u2663','8',8),(u'\u2663','9',9),(u'\u2660','10',10),(u'\u2663','J',10),(u'\u2663','Q',10),(u'\u2663','K',10)]
        random.seed()

    def next_card(self):
        if len(self.cards) == 0:
            raise DeckIsEmpty("Deck is empty.")
        card = random.randint(0, len(self.cards)-1)
        return self.cards.pop(card)
    
    @staticmethod
    def get_card_str(card):
        return card[0]+card[1]
    
    @staticmethod    
    def get_downcard_str():
        return Deck.downcard
        
#----------------------------CLASS HAND------------------------------------------------------
class Hand(object):
    def __init__(self, cards =[]):
        self.cards = cards
        self.bet = 0
    def add_card (self, card):
        self.cards.append(card)
    def get_value (self):
        return sum([x[2] for x in self.cards])
    def __unicode__ (self):
        return ''.join([Deck.get_card_str(c) for c in self.cards]) + ' ({:d})'.format(self.get_value())
    def __str__(self):
        return unicode(self).encode('utf-8')
    def __repr__(self):
        return self.__str__()
    def add_one_card(self, card, choose_a_value = True):
        new_card = card
        if card[1] == 'A' and choose_a_value:
            new_card = self.select_ace_value(card)
        self.cards.append(new_card)
        if choose_a_value:
            print "Updated hand: ", self
    def select_ace_value (self, card):
        print "Please select value of card "+Deck.get_card_str(card)
        while True:
            try:
                value = int(raw_input("(1 or 11?): "))
            except:
                continue
            else:
                if value != 1 and value != 11:
                    continue
                else:
                    return (card[0], card[1], value)
#----------------------------CLASS PLAYER------------------------------------------------------
class Player(object):
    def __init__(self, hand = Hand(), bank=100):
        self.bank = bank
        self.hands = [hand]
    def bet_on_hand(self, hand, amount):
        self.bank -= amount
        self.hands[hand].bet += amount
        
#----------------------------CLASS DEALER------------------------------------------------------    
class Dealer(object):
    def __init__(self, hand = Hand()):
        self.hand = hand

#----------------------------CLASS BLACKJACK----------------------------------------------------    
class BlackJack(object):
    STATE_NEW_ROUND = 0
    STATE_GAME_OVER = 1
    STATE_PLAYER_HAND = 2
    STATE_DEALER_HAND = 3
    STATE_END_OF_ROUND = 4
    STATE_EXIT = 5
    STATE_HIT = 6
    STATE_INSURANCE = 7
    STATE_DOUBLE_DOWN = 8
    STATE_SPLIT = 9
    STATE_HAND_START = 10
    STATE_END_OF_HAND = 11
    
    bet = 2.0
    
    def __init__(self):
        self.reset_game()
        pass
                

    def loose_if_more_than_21(self):
        if self.player.hands[self.current_hand].get_value() > 21:
            self.game_state = BlackJack.STATE_END_OF_HAND
            return True
        return False
    
    def win_if_black_jack(self):
        if self.player.hands[self.current_hand].get_value() == 21:
            self.game_state = BlackJack.STATE_END_OF_HAND
            return True
        return False
        
    def start(self):
        while True:
            self.available_commands = []
            
            if self.game_state == BlackJack.STATE_GAME_OVER:
                self.available_commands = [CommandExit(),CommandNewGame()]
                self.interact_with_user()
                continue

            if self.game_state == BlackJack.STATE_EXIT:
                break
            
            if self.game_state == BlackJack.STATE_END_OF_ROUND:
                print "Bank: ", self.player.bank
                print "-------------- END OF ROUND ---------------"
                if self.player.bank < BlackJack.bet:
                    print "You've lost all of your money. Game over!!!"
                    self.game_state = BlackJack.STATE_GAME_OVER
                else:
                    self.available_commands += [CommandContinue(),CommandExit(),CommandNewGame()]
                    self.interact_with_user()
                continue
                
            #----- NEW ROUND -----------------------------                                                                       
            if self.game_state == BlackJack.STATE_NEW_ROUND:
                self.deck = Deck()
                self.player.hands = [Hand([self.deck.next_card(), self.deck.next_card()])]
                self.dealer.hand = Hand([self.deck.next_card(), self.deck.next_card()])
                self.current_hand = 0
                
                self.player.hands = [Hand([(u'\u2660','2',2), (u'\u2666','2',2)])]
                self.dealer.hand = Hand([(u'\u2660','9',9), (u'\u2660','A',11)])
                
                # If dealer has two Aces, then one of them will be valued as 1
                if self.dealer.hand.get_value() == 22:
                    self.dealer.hand.cards[0][2] = 1
                
                if self.player.hands[self.current_hand].cards[0][1] == self.player.hands[self.current_hand].cards[1][1]:
                    self.available_commands.append(CommandSplit())
                                
                if self.dealer.hand.cards[1][1] == 'A' and self.player.bank >= 0.5*BlackJack.bet:
                    self.available_commands.append(CommandInsurance())

                print "-------------- NEW ROUND -----------------"
                print "Bank: ", self.player.bank
                print "Dealer hand:",Deck.get_downcard_str(), Deck.get_card_str(self.dealer.hand.cards[1])
                
                self.game_state = BlackJack.STATE_HAND_START
                if len(self.available_commands) != 0:
                    print "Your   hand:",self.player.hands[self.current_hand]
                    self.available_commands.append(CommandProceed())    
                    self.interact_with_user()
                continue


            #----- END OF HAND --------------------------
            if self.game_state == BlackJack.STATE_END_OF_HAND:
                if len(self.player.hands) == 2 and self.current_hand == 0:
                    self.current_hand = 1
                    self.game_state = BlackJack.STATE_HAND_START
                else:
                    self.game_state = BlackJack.STATE_DEALER_HAND
                continue

            #----- HIT CARD -----------------------------
            if self.game_state == BlackJack.STATE_HIT:
                self.player.hands[self.current_hand].add_one_card(self.deck.next_card())
                self.game_state = BlackJack.STATE_PLAYER_HAND
                continue

            #------ START HAND ---------------------------------
            if self.game_state == BlackJack.STATE_HAND_START:
                self.player.bet_on_hand(self.current_hand, BlackJack.bet)

                print "-------------- PLAY HAND -----------------"

                # Add additional cards if needed
                while len(self.player.hands[self.current_hand].cards) < 2:
                    self.player.hands[self.current_hand].add_one_card(self.deck.next_card(), False)

                print "Hand: ", self.player.hands[self.current_hand],"Bet:", self.player.hands[self.current_hand].bet
                
                # Select value of Ace
                for i in range(2):
                    if self.player.hands[self.current_hand].cards[i][1] == 'A':
                        self.player.hands[self.current_hand].cards[i] = self.player.hands[self.current_hand].select_ace_value(self.player.hands[self.current_hand].cards[i])
                        print "Updated hand: ", self.player.hands[self.current_hand]
                        
                self.game_state = BlackJack.STATE_PLAYER_HAND
                continue

            #----- SPLIT HANDS -------------------------------
            if self.game_state == BlackJack.STATE_SPLIT:
                self.player.hands.append(Hand([self.player.hands[0].cards.pop(1)]))
                self.game_state = BlackJack.STATE_HAND_START
                continue
            
            #----- DOUBLE DOWN -------------------------------
            if self.game_state == BlackJack.STATE_DOUBLE_DOWN:
                self.player.bet_on_hand(self.current_hand, BlackJack.bet)
                print "Your bet is doubled! New bet = {:.2f}".format(self.player.hands[self.current_hand].bet)
                self.player.hands[self.current_hand].add_one_card(self.deck.next_card())
                if self.loose_if_more_than_21() or self.win_if_black_jack():
                    continue
                else:
                    self.game_state = BlackJack.STATE_END_OF_HAND
                continue
            

            #----- DEALER HAND PLAYING ------------------------                               
            if self.game_state == BlackJack.STATE_DEALER_HAND:
                print "-------------- DEALER PLAYS --------------"
                while self.dealer.hand.get_value() < 17:
                    new_card = self.deck.next_card()
                    # Don't loose when getting an Ace
                    if new_card[1] == 'A' and self.dealer.hand.get_value > 10:
                        new_card = (new_card[0], new_card[1], 1)
                    self.dealer.hand.add_card(new_card)
                print "Dealer hand: ", self.dealer.hand
                for current_hand in self.player.hands:
                    print "Playing hand ", current_hand
                    if current_hand.get_value() > 21:
                        print "You have more than 21 and this hand looses."
                    elif current_hand.get_value() == 21:
                        print "You have a blackjack!"
                        self.player.bank += 1.5*self.player.hands[self.current_hand].bet
                    elif self.dealer.hand.get_value() < current_hand.get_value() or self.dealer.hand.get_value() > 21:
                        print "Hand wins! Your bet is doubled!"
                        self.player.bank += 2*current_hand.bet
                    elif self.dealer.hand.get_value() > current_hand.get_value():
                        print "Sorry, this hand looses."
                    elif self.dealer.hand.get_value() == current_hand.get_value():
                        print "Push! Your bet is returned to you."
                        self.player.bank += current_hand.bet
                    self.game_state = BlackJack.STATE_END_OF_ROUND
                continue

           #----- INSURANCE ----------------------------------   
            if self.game_state == BlackJack.STATE_INSURANCE:
                if self.dealer.hand.cards[0][2] == 10:
                    self.player.bank += 0.5*BlackJack.bet + self.player.hands[self.current_hand].bet
                    print "Your insurance wins. Dealer hand: ", self.dealer.hand
                    self.game_state = BlackJack.STATE_END_OF_ROUND
                else:
                    self.player.bank -= 0.5* BlackJack.bet
                    print "You are loosing your insurance."
                    self.game_state = BlackJack.STATE_HAND_START
                    # Split is possible after insurance is paied
                    if self.player.hands[self.current_hand].cards[0][1] == self.player.hands[self.current_hand].cards[1][1]:
                        self.available_commands += [CommandSplit(), CommandProceed()]
                        self.interact_with_user()
                    continue
 

            #----- PLAYER HAND INTERACTION -------------------------------
            if self.game_state == BlackJack.STATE_PLAYER_HAND:
                if self.win_if_black_jack():
                    continue
                if self.loose_if_more_than_21():
                    continue
                if 9 <= self.player.hands[self.current_hand].get_value() <= 11:
                    self.available_commands.append(CommandDoubleDown())

                if self.player.hands[self.current_hand].get_value() < 21:
                    self.available_commands.append(CommandHit())
                    self.available_commands.append(CommandStand())
                self.interact_with_user()
                continue
                               
                
    def interact_with_user(self):
        #Interaction with user
        print self.available_commands
        
        while True:
            user_input = raw_input("Please enter command:")    
            try:
                self.execute_command(user_input)
            except (InvalidInput):
                print "Sorry, unknown or unavailable command ", user_input
                continue
            else:
                break
        
    def execute_command(self, user_input):
        for command in self.available_commands:
            if command.activation_str != user_input:
                continue
            if type(command) == CommandExit:
                self.game_state = BlackJack.STATE_EXIT
                return
            elif type(command) == CommandNewGame:
                self.reset_game()
                return
            elif type(command) == CommandHit:
                self.game_state = BlackJack.STATE_HIT
                return
            elif type(command) == CommandStand:
                self.game_state = BlackJack.STATE_END_OF_HAND
                return
            elif type(command) == CommandContinue:
                self.game_state = BlackJack.STATE_NEW_ROUND
                return
            elif type(command) == CommandInsurance:
                self.game_state = BlackJack.STATE_INSURANCE
                return
            elif type(command) == CommandDoubleDown:
                self.game_state = BlackJack.STATE_DOUBLE_DOWN
                return
            elif type(command) == CommandSplit:
                self.game_state = BlackJack.STATE_SPLIT
                return
            elif type(command) == CommandProceed:
                return
        raise InvalidInput("Unknown command")
        
    def reset_game(self):
        self.dealer = Dealer()
        
        while True:
            try:
                bank = int(raw_input("How much money do you want to spend today?"))
            except:
                print "Entered value is incorrect. Please try again."
                continue
            else:
                self.player = Player(bank = bank)
                break
                
        self.game_state = BlackJack.STATE_NEW_ROUND

def main():
    try:
        print u'\u2660\u2660\u2660\u2660\u2660', " Welcome to BlackJack! ",u'\u2660\u2660\u2660\u2660\u2660' 
    except:
        print "It seems your terminal doesn't support unicode characters."
        print "If you are using MS Windows please try to run this program in Cygwin."
        return
    game = BlackJack()
    game.start()
	
if __name__ == '__main__':
	main()

