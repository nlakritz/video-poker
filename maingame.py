# Nathan Lakritz
# Fall 2016
# natejl123@gmail.com

import random
import VideoPoker

def create_deck():
    '''Creates a deck of cards by storing character pairs into a list.
    The elements are then randomized with a random shuffle function.'''
    suits = "CDHS"  # String of suits.
    ranks = "23456789TJQKA"  # String of ranks.
    deck = []
    for i in range(len(suits)):
        for j in range(len(ranks)):
            deck.append(ranks[j] + suits[i])
    random.shuffle(deck)
    return deck


def create_hand(deck):
    ''' Sets a player's hand based off the first 5 elements of the deck.'''
    hand = deck[:5]
    deck[:5] = []  # Need to remove hand from deck.
    return hand


def suit_string(s):
    '''Creates a string that represents suit frequencies.'''
    frequencies = list(s.items())
    suit_string = ""
    for x in frequencies:
        suit_string += str(x[1])  # Appending single suit frequencies.
    return suit_string


def rank_string(r):
    '''Creates a string that represents rank frequencies.'''
    frequencies  = list(r.items())
    rank_string = ""
    for x in frequencies:
        rank_string += str(x[1])
    return rank_string


def outcome(suits, ranks):
    '''Determines outcome of player's hand.'''
    for x in suits:
        if x == "5":  # If all suits are the same, there has to be some type of flush.
            if ranks[8] == "1" and ranks[9] == "1" and ranks[10] == "1" and ranks[11] == "1" and ranks[12] == "1":  # Checking for the specific cards required for a royal flush.
                ranking = "Royal Flush"
            elif ranks.count("11111") == 1:  # Five consecutive cards means there is a straight flush.
                ranking = "Straight Flush"
            else:
                ranking = "Flush"  # If the flush isn't royal or straight, it's standard.
            return ranking
    for y in ranks:
        if y == "4":  # Checking for a frequency of four for any given card.
            ranking = "Four of a Kind"
            return ranking
        elif y == "3":
            if ranks.count("2") == 1:  # Checking for a full house before a three of a kind because it's better.
                ranking = "Full House"
            elif ranks.count("2") == 0:
                ranking = "Three of a Kind"
            return ranking
    if ranks.count("11111") == 1:  # Regular straight
        ranking = "Straight"
    elif ranks.count("2") == 2:
        ranking = "Two Pair"
    elif ranks[9] == "2" or ranks[10] == "2" or ranks[11] == "2" or ranks[12] == "2":  # Jacks or better.
        ranking = "Pair"
    else:
        ranking = "Nothing"  # The function will only get here if it hasn't returned a winning hand.
    return ranking


starting_credits = int(input("How many credits would you like to start with? (10-1000) "))
while starting_credits < 10 or starting_credits > 1000:  # Input validation
    starting_credits = int(input("How many credits would you like to start with? (10-1000) "))
vp = VideoPoker.VideoPoker()  # Initiating video poker graphics.
vp.set_status("Hello and Welcome to Video Poker!")


def poker_round(credits, deck):
    '''Runs a round of poker and keeps the user updated on game status.
    Current credit balance is updated based on gameplay.
    Deck is from poker_game(), which runs a deck-builder function as needed.'''
    vp.display_credits(credits)  # Displaying starting credits.
    bet = vp.get_credits_bet()  # Taking user's bet (1-5 credits).
    while bet > credits:
        vp.set_status("You do not have enough credits for that bet. Bet again.")
        bet = vp.get_credits_bet()
    vp.set_status("You bet " + str(bet) + " credits.")  # Updating game status.
    credits = credits - bet  # Decreasing user's credit balance.
    vp.display_credits(credits)  # Updating the credit balance on-screen.
    hand = create_hand(deck)  # Creating a hand based on the given deck.
    vp.set_cards(hand)  # Setting the displayed cards to the hand.
    holding = vp.get_held_cards()  # Generating a list containing cards the user chooses to keep.

    # Drawing cards from the original deck to replace the cards that aren't held by the user.
    for x in range(0, 5):
        if holding.count(x) != 1:
            hand[x] = deck[0]
            deck.pop(0)
    vp.set_cards(hand)  # Setting the displayed cards to the updated hand.

    suit_dic = {"C": 0, "D": 0, "H": 0, "S": 0}
    for i in range(len(hand)):
        suit_dic[hand[i][1]] += 1  # Adding frequencies
    rank_dic = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "T": 0, "J": 0, "Q": 0, "K": 0, "A": 0}
    for j in range(len(hand)):
        rank_dic[hand[j][0]] += 1
    s = suit_string(suit_dic)  # Converting dictionaries to strings.
    r = rank_string(rank_dic)
    result = outcome(s, r)

    if result == "Royal Flush":  # Reading result string.
        if bet != 5:
            new_bal = (bet * 250) + credits  # Multiplying bet by designated credit amount and then adding previous balance to create new balance.
            vp.set_status("You got a ROYAL FLUSH!!!! You have earned " + str(bet * 250) + " credits!")  # Updating game status.
        elif bet == 5:  # Special payout case.
            new_bal = 4000 + credits
            vp.set_status("You got a ROYAL FLUSH!!!! You have earned " + str(4000) + " credits!")
    elif result == "Straight Flush":
        new_bal = (bet * 50) + credits
        vp.set_status("You got a Straight Flush! You have earned " + str(bet * 50) + " credits!")
    elif result == "Four of a Kind":
        new_bal = (bet * 25) + credits
        vp.set_status("You got a Four of a Kind! You have earned " + str(bet * 25) + " credits!")
    elif result == "Full House":
        new_bal = (bet * 9) + credits
        vp.set_status("You got a Full House! You have earned " + str(bet * 9) + " credits!")
    elif result == "Flush":
        new_bal = (bet * 6) + credits
        vp.set_status("You got a Flush! You have earned " + str(bet * 6) + " credits!")
    elif result == "Straight":
        new_bal = (bet * 4) + credits
        vp.set_status("You got a Straight! You have earned " + str(bet * 4) + " credits!")
    elif result == "Three of a Kind":
        new_bal = (bet * 3) + credits
        vp.set_status("You got a Three of a Kind! You have earned " + str(bet * 3) + " credits!")
    elif result == "Two Pair":
        new_bal = (bet * 2) + credits
        vp.set_status("You got Two Pairs! You have earned " + str(bet * 2) + " credits!")
    elif result == "Pair":
        new_bal = (bet * 1) + credits
        vp.set_status("You got One Pair! You have earned " + str(bet * 1) + " credit(s)!")
    elif result == "Nothing":
        new_bal = credits
        vp.set_status("You got NOTHING. You have earned NO credits :(")
    vp.display_credits(new_bal)  # Showing the user their new balance if it changed.
    vp.await_continue_button()  # Waiting for the user to continue before starting another round.
    return new_bal  # Credit amount to be reused for next round.


def poker_game(balance):
    '''Lets the user play a game of poker until they run out of credits.'''
    deck = create_deck()
    while True:
        if balance <= 0:
            break
        elif len(deck) < 10: # Shuffle a new deck if there aren't enough cards for another round.
            deck = create_deck()
        balance = poker_round(balance, deck)


poker_game(starting_credits)  # Starting the game cycle by calling the main function.
print("You have run out of credits! GAME OVER.")
