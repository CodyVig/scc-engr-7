""" 
Defines the functions to play a (simplified) game of 21 
"""

from random import sample


def new_deck():
    """
    Return a set of tuples representing a deck of cards.
    Tuples are (card value, card suit)
    """

    vals = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "jack",
        "queen",
        "king",
        "ace",
    ]
    suits = ["spades", "clubs", "hearts", "diamonds"]
    deck = set([(v, s) for v in vals for s in suits])
    return deck


def deal_cards(d, n=2):
    """
    Returns a hand of n cards taken from the deck d.
    The hand and deck are both represented by a set of tuples.
    The deck d is updated to remove the two randmoly selected cards.
    Uses sample() from the random module.

    Inputs
        d   -   deck of cards, a set of tuples.
        n   -   the number of cards to draw from the deck

    Returns:
        hand - set of n tuples representing cards
    """
    hand = set(sample(list(d), n))

    for card in hand:
        d.remove(card)

    return hand


def display_hand(hand):
    """
    Prints the hand and best score for the hand.

    Inputs:
        hand - set of tuples representing a card (value, suit)
    """

    for card in hand:
        v = card[0]
        s = card[1]

        print("\t", v, " of ", s)
    print("\tBest score = ", best_score(hand))


def best_score(hand):
    """
    Returns the best score of a hand based on its
    Cards with values 1- 9 have their value as their score
    Cards that are Jack, Queen, or king have score 10
    Cards that are aces are either 1 or 10 depending on which
    produces the best score.

    The best score is the largest possible score that is <= 21.

    Inputs
        hand - a set of tuples representing cards
                (first entry is the value, second is the suit)

    Returns
        best_score - best possible score for the hand
    """

    # count the number of aces and the total score without aces
    score_without_aces = 0
    number_of_aces = 0

    ####### Your code for Problem 1 goes here #######
    ### Add code to calculate score_without_aces (currently set to 0)
    for card in hand:
        # If we can convert card[0] to an `int`, then it is "2" though "10"
        try:
            score_without_aces += int(card[0])
        # Otherwise, it is "jack", "queen", "king", or "ace".
        except ValueError:
            if card[0] in ["jack", "queen", "king"]:
                score_without_aces += 10
            elif card[0] == "ace":
                number_of_aces += 1
            else:
                # If we made it here, this is not a valid card value
                raise ValueError(f"Invalid card value in {card}")

    # now deal with the aces (if any) and find the best score
    if number_of_aces == 0:
        best_score = score_without_aces

    # 1 ace, either add 10 or 1
    elif number_of_aces == 1:
        if score_without_aces + 10 <= 21:
            best_score = score_without_aces + 10
        else:
            best_score = score_without_aces + 1

    # 2 aces, we either add 20, 11, or 2
    elif number_of_aces == 2:
        if score_without_aces + 20 <= 21:
            best_score = score_without_aces + 20
        elif score_without_aces + 11 <= 21:
            best_score = score_without_aces + 11
        else:
            best_score = score_without_aces + 2

    # 3 aces, either add 21, 12, or 3
    elif number_of_aces == 3:
        if score_without_aces + 21 <= 21:
            best_score = score_without_aces + 21
        elif score_without_aces + 12 <= 21:
            best_score = score_without_aces + 12
        else:
            best_score = score_without_aces + 3

    # 4 aces we can only have 13 or 4
    else:
        if score_without_aces + 13 <= 21:
            best_score = score_without_aces + 10 + 3
        else:
            best_score = score_without_aces + 4

    return best_score


def strategy_stop_at(hand, n, *args, **kwargs):
    """
    Returns True or False depending on whether the customer should
    continue or not. Continue if the customer score <= n (return True)
    return False otherwise

    Inputs
        hand     -  set of tuples representing cards
        n        -  an integer

    Variable arguments are allowed so that we may generalize `play_21`.
    """

    if best_score(hand) < n:
        return True
    else:
        return False


def strategy_dealer_sensitive(hand, card, *args, **kwargs):
    """
    Returns True or False depending on whether the costomer should
    continue or not.

    Continue in the case that
        * card is an ace, 7, 8, 9, 10, king, queen, or jack AND
          the best_score of hand has less than 17 OR
        * card is a 2, 3, 4, 5, or 6 AND the customer has less than 12.

    Return False in all other cases

    Inputs
        hand     -  set of tuples representing cards
        card     -  tuple representing the visible card of the dealer

    Variable arguments are allowed so that we may generalize `play_21`.
    """

    if (
        card[0] in ["7", "8", "9", "10", "king", "queen", "jack", "ace"]
        and best_score(hand) < 17
    ):
        return True
    elif card[0] in ["2", "3", "4", "5", "6"] and best_score(hand) < 12:
        return True
    return False


def strategy_conservative(hand, card, *args, **kwargs):
    """
    Returns True or False depending on whether the customer should
    continue or not.

    * Only return True in the case that both strategy_stop_at(hand, 15) and
        strategy_dealer_sensitive return true.
    * Return False in all other cases

    Inputs:
        hand     -  set of tuples representing cards
        card     -  tuple representing the visible card of the dealer
    """

    return strategy_stop_at(hand, 15) and strategy_dealer_sensitive(hand, card)


def play_21(verbose: bool = True, strategy: str = "default"):
    """
    Play a game of twenty one!
    Return True if customer wins and False otherwise.

    :param verbose: Whether the print statements should be run.
    :param strategy: The strategy function to be used. Options are:
        - "default": uses `strategy_stop_at(customer_hand, 17)`
        - "sensitive": uses `strategy_dealer_sensitive()`
        - "conservative": uses `strategy_dealer_conservative()`
    """

    if strategy.lower().strip() == "sensitive":
        strategy_function = strategy_dealer_sensitive
    elif strategy.lower().strip() == "conservative":
        strategy_function = strategy_conservative
    elif strategy.lower().strip() == "default":
        strategy_function = strategy_stop_at
    else:
        print(
            f"argument {strategy=} in `play_21` unknown."
            + " Using default strategy."
        )
        strategy_function = strategy_stop_at

    if verbose:
        print("*********************************")
        print("~~~~~~~~~~~ Playing 21 ~~~~~~~~~~")
        print("*********************************\n")

    # create a deck of cards
    deck = new_deck()

    # deal 2 cards to the customer
    customer_hand = deal_cards(deck, 2)

    # deal 2 cards to the dealer
    dealer_hand = deal_cards(deck, 2)

    if verbose:
        # game continues as long as the customer decided to keep drawing a card
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~ Initial Hands ~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        print("Customer's hand")
        display_hand(customer_hand)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Dealer's hand")
        display_hand(dealer_hand)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # sets don't have order, so convert to list and pick the first entry as the
    # visible card
    dealer_visible_card = list(dealer_hand)[0]
    if verbose:
        print("Dealer's visible card is", dealer_visible_card)

    while strategy_function(hand=customer_hand, card=dealer_visible_card, n=17):
        # pick a card for customer
        customer_hand.update(deal_cards(deck, 1))
        if verbose:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("*** Customer has picked a card ***")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Customer's hand")
            display_hand(customer_hand)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # check if new card sent customer over 21
        if best_score(customer_hand) > 21:
            if verbose:
                print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")
            return False

        # now dealer will decide to choose a card
        if strategy_function(
            hand=customer_hand, card=dealer_visible_card, n=17
        ):
            dealer_hand.update(deal_cards(deck, 1))
            if verbose:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("*** Dealer has picked a card ***")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Dealer's hand")
                display_hand(dealer_hand)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # check if the new card sent the dealer over 21
            if best_score(dealer_hand) > 21:
                if verbose:
                    print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")
                return False

        # check if customer won (has exactly 21)
        if best_score(customer_hand) == 21:
            if verbose:
                print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")
            return True

        # check if dealer has won (has exactly 21)
        elif best_score(dealer_hand) == 21:
            if verbose:
                print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")
            return False

        # check if there is a tie
        elif best_score(customer_hand) == 21 and best_score(dealer_hand) == 21:
            if verbose:
                print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")
            return False

    if verbose:
        print("~~~~~~~~~~GAME HAS ENDED~~~~~~~~~~")

    # customer stopped choosing cards so check if they won
    if (best_score(customer_hand) == 21) and (best_score(dealer_hand) == 21):
        return False

    elif best_score(customer_hand) > best_score(dealer_hand):
        return True

    else:
        return False


def play_n(n, strategy: str = "default"):
    """
    Play 21 n times! This function will call play_21 a total of
    n times and return the number of times the customer wins.

    Returns the number of customer wins (out of n)
    """

    num_wins = 0
    for _ in range(n):
        win = play_21(verbose=False, strategy=strategy)
        num_wins += 1 if win else 0

    return num_wins


###### Helper functions to test code below ######
###### No need to read these .... ######


def test_best_score():
    """
    Test the best score function
    """
    hand = {("queen", "clubs"), ("6", "diamonds"), ("10", "hearts")}
    if not best_score(hand) == 26:
        print("**** best_score() failed on hand ", hand)
    else:
        print("best_score() passed on test case!")

    hand = {("7", "spades"), ("9", "clubs"), ("6", "diamonds")}
    if not best_score(hand) == 22:
        print("**** best_score() failed on hand ", hand)
    else:
        print("best_score() passed on test case!")

    hand = {
        ("2", "hearts"),
        ("8", "diamonds"),
        ("2", "clubs"),
        ("3", "hearts"),
        ("9", "diamonds"),
    }
    if not best_score(hand) == 24:
        print("**** best_score() failed on hand ", hand)
    else:
        print("best_score() passed on test case!")

    hand = {
        ("ace", "hearts"),
        ("10", "hearts"),
        ("3", "hearts"),
        ("ace", "spades"),
    }
    if not best_score(hand) == 15:
        print("**** best_score() failed on hand ", hand)
    else:
        print("best_score() passed on test case!")


def test_strategy_dealer_sensitive():
    """
    Test the strategy_dealer_sensitive function
    """

    hand = {("queen", "clubs"), ("6", "diamonds"), ("10", "hearts")}
    dealer_visible_card = ("king", "hearts")

    if strategy_dealer_sensitive(hand, dealer_visible_card) is not False:
        print("**** strategy_dealer_sensitive() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_dealer_sensitive() passed on test case!")

    hand = {("4", "diamonds"), ("2", "clubs")}
    dealer_visible_card = ("2", "spades")

    if strategy_dealer_sensitive(hand, dealer_visible_card) is not True:
        print("**** strategy_dealer_sensitive() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_dealer_sensitive() passed on test case!")

    hand = {("10", "spades"), ("1", "clubs"), ("2", "diamonds")}
    dealer_visible_card = ("ace", "hearts")

    if strategy_dealer_sensitive(hand, dealer_visible_card) is not True:
        print("**** strategy_dealer_sensitive() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_dealer_sensitive() passed on test case!")

    hand = {("10", "spades"), ("1", "clubs"), ("2", "diamonds")}
    dealer_visible_card = ("2", "hearts")

    if strategy_dealer_sensitive(hand, dealer_visible_card) is not False:
        print("**** strategy_dealer_sensitive() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_dealer_sensitive() passed on test case!")


def test_strategy_conservative():
    """
    Test the strategy_dealer_sensitive function
    """

    hand = {("queen", "clubs"), ("6", "diamonds"), ("10", "hearts")}
    dealer_visible_card = ("king", "hearts")

    if strategy_conservative(hand, dealer_visible_card) is not False:
        print("**** strategy_conservative() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_conservative() passed on test case!")

    hand = {("4", "diamonds"), ("2", "clubs")}
    dealer_visible_card = ("2", "spades")

    if strategy_conservative(hand, dealer_visible_card) is not True:
        print("**** strategy_conservative() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_conservative() passed on test case!")

    hand = {("10", "spades"), ("1", "clubs"), ("2", "diamonds")}
    dealer_visible_card = ("2", "hearts")

    if strategy_conservative(hand, dealer_visible_card) is not False:
        print("**** strategy_conservative() failed ***")
        print("\t Hand ", hand)
        print("\t Dealer visible card", dealer_visible_card)
    else:
        print(" strategy_conservative() passed on test case!")
