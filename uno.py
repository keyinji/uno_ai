# Author: Evan Luo, Ke Yin Ji
# Base function: multiplayer
# Merged with reshuffle (Evan Luo)
import random

colours = ("Red", "Yellow", "Blue", "Green")
ranks = list(range(1, 11))

deck = [(rank, colour) for rank in ranks for colour in colours]

random.shuffle(deck)


# Game Setup
print("Welcome to UNO!")

player_number_input = input("How many players? (2-4): ")

while not player_number_input.isdigit() or not (2 <= int(player_number_input) <= 4):
    print("Invalid input. Please input a number between 2 and 4")
    player_number_input = input("How many players? (2-4): ")

player_number = int(player_number_input)

print(f"Number of players: {player_number}")

print("Config done. Let's start the game!")

def valid_play(face_up, card):
    face_up_rank = face_up[-1][0]
    face_up_colour = face_up[-1][1]
    card_rank = card[0]
    card_colour = card[1]

    return face_up_rank == card_rank or face_up_colour == card_colour

def start_game(deck, player_number):
    face_up = [deck.pop(0)]
    main_loop(player_number, face_up, deck)

def valid_index(index, hand):
    return 0 <= index < len(hand)

def print_drew_card(current_hand):
    print(f"You drew: [{current_hand[-1][1]} {current_hand[-1][0]}]")

def next_player(current_player, total_players_count):
    return (current_player + 1) % total_players_count

def main_loop(total_players_count, face_up, deck_data):
    player_hand = [[deck_data.pop(0) for _ in range(7)] for _ in range(total_players_count)]
    current_player = 0

    while True:
        current_player_number = current_player + 1
        current_hand = player_hand[current_player]

        print("")
        print("=====================================")
        print(f"Player {current_player_number}'s turn")
        print("=====================================")
        print(f"\nFace up card: [{face_up[-1][1]} {face_up[-1][0]}]")

        print(f"\nYour hand:")
        print(f"Index: Card")
        for card in current_hand:
            print(f"{current_hand.index(card) + 1}: [{card[1]} {card[0]}]")

        print("\nDo you want to play or draw a card?")
        print("Press index of the card you wanna play, or d for draw")
        if current_player_number == 2:
            ai_play(current_hand, face_up)
            current_player = next_player(current_player, total_players_count)
            continue
        user_choice = input("Your choice (card index/d): ")

        while (user_choice != "d") and (not user_choice.isdigit()):
            print("Invalid input. Try again")
            user_choice = input("Your choice (card index/d): ")

        if user_choice == "d": # Draw the card
            if len(deck_data) == 0:
                if len(face_up) <= 1:
                    print("No cards left to draw. Game over")
                    break
                print("Deck is empty. Shuffling face up cards")
                deck_data = face_up[:-1]
                random.shuffle(deck_data)
                face_up = [face_up[-1]]
            current_hand.append(deck_data.pop(0))
            print_drew_card(current_hand)
        else: # Play the card
            card_chose_index = int(user_choice) - 1
            if not valid_index(card_chose_index, current_hand):
                print("Index out of range. Draw a card instead")
                current_hand.append(deck_data.pop(0))
                print_drew_card(current_hand)
                current_player = next_player(current_player, total_players_count)
                continue

            card_chosen = current_hand[card_chose_index]
            is_valid = False
            while not is_valid:
                is_valid = valid_play(face_up, card_chosen)
                print(f"You chose: [{card_chosen[1]} {card_chosen[0]}]")

                if not is_valid:
                    card_chose_index = input("Card not valid. Choose index again: ")
                    if card_chose_index == "d":
                        print("Drawing a card...")
                        current_hand.append(deck_data.pop(0))
                        print_drew_card(current_hand)
                        current_player = next_player(current_player, total_players_count)
                        break
                    if not card_chose_index.isdigit() or not valid_index(int(card_chose_index) - 1, current_hand):
                        print("Invalid input. Try again")
                        card_chose_index = input("Card not valid. Choose index again: ")
                        continue
                    card_chose_index = int(card_chose_index) - 1
                    card_chosen = current_hand[card_chose_index]

            if not is_valid:
                continue
            current_hand.pop(card_chose_index)
            face_up.append(card_chosen)
            if not current_hand:
                print("\n\n=====================================")
                print(f"Player {current_player_number} wins!")
                print("=====================================")
                break

        current_player = next_player(current_player, total_players_count)

def ai_play(ai_deck, face_up):
    for card in ai_deck:
        if valid_play(face_up, card):
            print(f"AI played: [{card[1]} {card[0]}]")
            ai_deck.remove(card)
            face_up.append(card)
            return
    print("AI drew a card")
    ai_deck.append(deck.pop(0))


start_game(deck, player_number)
