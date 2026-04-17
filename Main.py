import pygame
import random
import time
from random import randint
from itertools import repeat
import pygame.gfxdraw
import math

########################
#Variables and Settings#
########################

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
background = pygame.image.load("Assets/Background.png")
SCALE_FACTOR = 1
NEW_SCALER = 1440/1980
SCREEN_WIDTH, SCREEN_HEIGHT = 1440*SCALE_FACTOR, 840*SCALE_FACTOR
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("BlackJack")

# Music choices
music_choices = ["Music/Music1.mp3", "Music/Music2.mp3", "Music/Music3.mp3"]

music = random.choice(music_choices)
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Sounds
hit_sound = pygame.mixer.Sound("Sounds/Hit.mp3")
joker_sound = pygame.mixer.Sound("Sounds/Joker.mp3")
lose_sound = pygame.mixer.Sound("Sounds/Lose.mp3")
shuffle_sound = pygame.mixer.Sound("Sounds/Shuffle.mp3")
stand_sound = pygame.mixer.Sound("Sounds/Stand.mp3")
start_sound = pygame.mixer.Sound("Sounds/Start.mp3")
win_sound = pygame.mixer.Sound("Sounds/Win.mp3")

# Game start
game_active = 0
start_bg = pygame.image.load("Assets/Background2.png")
start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_bg_rect = start_bg.get_rect(topleft = (0, 0))

made_by = pygame.image.load("Assets/Made.png")
made_by = pygame.transform.scale(made_by, (50, 30))
made_by_rect = made_by.get_rect(center = (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100))
made_by_text = pygame.font.Font("Assets/BalatroFont.ttf", 20)

# lose screen
lose_screen = pygame.image.load("Assets/lobby.jpg")
lose_screen = pygame.transform.scale(lose_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
lose_screen_rect = lose_screen.get_rect(topleft = (0, 0))

logo = pygame.image.load("Assets/BlackJack Modifier Engine Logo.png")
logo = pygame.transform.scale(logo, (550, 550))
logo_rect = logo.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))

start_text = pygame.font.Font("Assets/BalatroFont.ttf", 75)
start_writing = start_text.render("Press Space to start game", True, "#ff0000")
start_writing_rect = start_writing.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 100))
end_text = pygame.font.Font("Assets/BalatroFont.ttf", 175)

logo_speed = 1
logo_acceleration = 0
first_speed = 0

def start_game():
    global logo_speed
    screen.blit(start_bg, start_bg_rect)
    screen.blit(logo, logo_rect)
    screen.blit(start_writing, start_writing_rect)
    logo_rect.y += logo_speed

    # movement of logo
    if logo_rect.y >= 130:
        logo_speed = -1
    elif logo_rect.y <= 60:
        logo_speed = 1
    
# Win lose
def win_lose():
    global game_active, money_amount
    if money_amount <= 0:
        game_active = 2
    if game_active == 2:
        end_text = pygame.font.Font("Assets/BalatroFont.ttf", 100)
        end_writing = end_text.render(f'You lose!\nYour Score: {roundnumber}', True, "#00A550")
        end_writing_rect = start_writing.get_rect(center = (SCREEN_WIDTH/2 + 100, SCREEN_HEIGHT/2 - 50))
        screen.blit(lose_screen, lose_screen_rect)
        screen.blit(end_writing, end_writing_rect)

# Card size
CARD_WIDTH = 155
CARD_HEIGHT = int(CARD_WIDTH * 1164 / 876)  # Maintain aspect ratio

# Side Bar
SIDEBAR_WIDTH = 390

# Global variables for game states, values, and hands
dealer_hand = []
player_hand = []
player_valued_hand = []
dealer_valued_hand = []
player_positions = []
player_value = 0
dealer_value = 0
bust_value = 21
dealer_bust_value = 21
dealer_breakthrough = False
player_breakthrough = False
hit_enabled = False  # Hit button initially disabled
stand_enabled = False
dealer_aces = 0
player_aces = 0
joker = False
money_amount = 1000
bet = 100
money_multiplier = 1.0
player_card_multiplier = 1
dealer_card_multiplier = 1
player_value_multiplier = 1.0
dealer_value_multiplier = 1.0
is_duality = False
is_duality_dealer = False
is_timestopped = False
is_timestopped_dealer = False
is_infernal = False
number_of_hits = 0
ascension_limit = 2
ascension = False
ascension_dealer = False
deck_number = 104
roundnumber = 1
status = None

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
hit_button_rect = pygame.Rect((SCREEN_WIDTH // 2) - 16, SCREEN_HEIGHT - 90, BUTTON_WIDTH + 30, BUTTON_HEIGHT+30)
stand_button_rect = pygame.Rect((SCREEN_WIDTH // 2) + BUTTON_WIDTH + 38, SCREEN_HEIGHT - 90, BUTTON_WIDTH +30, BUTTON_HEIGHT+30)

# Joker settings
JOKER_TYPES = {
    43: "Ascension",
    44: "Dead man's hand",
    45: "Duality",
    46: "Multiplier 1.1x",
    47: "Multiplier 1.2x",
    48: "Multiplier 1.3x",
    49: "Multiplier 1.4x",
    66: "Jackpot",
    33: "Malice",
    74: "Infernal",
    105: "Cosmic",
    35: "Entity Beyond Time",
    50: "Breakthrough",
    1: "Normal",
    65: "Null",
    11: "The King",
    12: "The King",
    63: "The Ruler",
    104: "The One",
    120: "Gift of Heavens",
    153: "The One Above All"
}

RARE_LIST = [49,63,66,104,50,44,74,105,120,65,33,43,153,35]

CUTSCENE = {}

# Joker rarities (Divide by 100) -> Percentage
JOKER_RARITIES = {
    #Common 40%
    1: 1333,
    46: 1333,
    47: 1333,
    #Rare 30%
    45: 750,
    48: 750,
    11: 750,
    12: 750,
    #Epic 20%
    49: 667,
    66: 667,
    63: 667,
    #Legendary 13%
    104: 325,
    74: 325,
    44: 325,
    50: 325,
    #Mythical 5%
    105: 100,
    120: 100,
    65: 100,
    33: 100,
    43: 100,
    #Godly 2%
    153:100,
    35: 100
}

###############
#Initiate Game#
###############

# Load card images
def load_card_images():
    card_images = {}
    suits = ["h", "c", "d", "s"]
    base_path = "Media/Cards/DEFFAULT/"
    steel_path = "Media/Cards/STEEL/"
    gold_path = "Media/Cards/GOLD/"

    for suit_index, suit in enumerate(suits):
        for value in range(1, 14):  # 1 (2) to 13 (Ace)
            # Card number in the folder
            card_number = (suit_index * 13) + value

            if value == 1:
                card_name = f"2{suit}"  # 2
            elif value == 10:
                card_name = f"j{suit}"  # Jack
            elif value == 11:
                card_name = f"q{suit}"  # Queen
            elif value == 12:
                card_name = f"k{suit}"  # King
            elif value == 13:
                card_name = f"a{suit}"  # Ace
            else:
                card_name = f"{value + 1}{suit}"  # Numeric cards (3 to 10)

            original_image = pygame.image.load(f"{base_path}8BitDeck{card_number}.png")
            steel_original_image = pygame.image.load(f"{steel_path}8BitDeck{card_number}.png")
            gold_original_image = pygame.image.load(f"{gold_path}8BitDeck{card_number}.png")
            resized_image = pygame.transform.scale(original_image, (CARD_WIDTH, CARD_HEIGHT))
            resized_image_steel = pygame.transform.scale(steel_original_image, (CARD_WIDTH, CARD_HEIGHT))
            resized_image_gold = pygame.transform.scale(gold_original_image, (CARD_WIDTH, CARD_HEIGHT))
            card_images[card_name] = resized_image
            card_images[f"steel{card_name}"] = resized_image_steel
            card_images[f"gold{card_name}"] = resized_image_gold

    # Load joker images
    for joker_number in JOKER_TYPES.keys():
        joker_image = pygame.image.load(f"Media/Joker/Jokers{joker_number}.png")
        resized_joker = pygame.transform.scale(joker_image, (CARD_WIDTH, CARD_HEIGHT))
        card_images[f"Joker{joker_number}"] = resized_joker

    # Back of the card
    back_image = pygame.image.load("Media/Cards/Back.png")
    card_images["back"] = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))

    # Null cards
    null_image = pygame.image.load("Media/Cards/Null.png")
    card_images["Null"] = pygame.transform.scale(null_image, (CARD_WIDTH, CARD_HEIGHT))
    return card_images

# Generate deck
def generate_deck():
    suits = ["h", "c", "d", "s"]
    values = [str(v) for v in range(2, 11)] + ["j", "q", "k", "a"]
    single_deck = [f"{v}{s}" for s in suits for v in values]
    full_deck = single_deck * 2

    # Add 12 jokers to the deck
    full_deck += ["Joker"] * 36
    random.shuffle(full_deck)
    return full_deck

# Determine joker type
def determine_joker_type():
    total_rarity = sum(JOKER_RARITIES.values())
    rand_num = random.randint(1, total_rarity)
    cumulative_rarity = 0

    for joker_number, rarity in JOKER_RARITIES.items():
        cumulative_rarity += rarity
        if rand_num <= cumulative_rarity:
            return joker_number

    return 1  # Default to normal joker if something goes wrong

############
#First Deal#
############

# Calculate positions for first 4 cards
def calculate_first_deal_positions():
    global background, SIDEBAR_WIDTH
    positions = {"dealer": [], "player": []}
    total_width = 2 * CARD_WIDTH + 20
    playable_width = SCREEN_WIDTH - SIDEBAR_WIDTH
    dealer_x_start = SIDEBAR_WIDTH + (playable_width - total_width) // 2

    for i in range(2):  # Two initial cards
        x = dealer_x_start + i * (CARD_WIDTH + 20) - 20
        positions["dealer"].append((x, 75))
        positions["player"].append((x, SCREEN_HEIGHT - 80 - CARD_HEIGHT))

    return positions

# Animation
def first_deal():
    global player_positions, hit_enabled, stand_enabled, player_value, dealer_value, bust_value, is_timestopped
    global joker, RARE_LIST, dealer_valued_hand, player_valued_hand, player_card_multiplier, dealer_card_multiplier, is_duality, is_duality_dealer
    global background

    card_positions = calculate_first_deal_positions()
    player_positions = card_positions["player"][:]
    hands = [player_hand, dealer_hand, player_hand, dealer_hand]

    for i, hand in enumerate(hands):
        while True:
            card_key = deck.pop() if i != 3 else "back"
            if not joker and card_key == "Joker":
                deck.insert(0, card_key)
                random.shuffle(deck)
                continue
            break

        # Position
        start_pos = (SCREEN_WIDTH, -200)
        end_pos = card_positions["player" if i % 2 == 0 else "dealer"][len(hand)]

        if card_key == "Joker":
            card_image = card_images["Joker1"]
            joker_type = determine_joker_type()
            reveal_joker(joker_type, end_pos, is_player=(i % 2 == 0), is_first_deal=True)
        else:
            card_image = card_images[card_key]

            # Animate
            clock = pygame.time.Clock()
            steps = 500 // 24
            for step in range(steps + 1):
                t = step / steps
                x = int(start_pos[0] + t * (end_pos[0] - start_pos[0]))
                y = int(start_pos[1] + t * (end_pos[1] - start_pos[1]))

                screen.blit(background, (0, 0))
                draw_all_cards()
                draw_value_boxes()
                screen.blit(card_image, (x, y))
                pygame.display.flip()
                clock.tick(60)

            hand.append(card_key)

            # **Fix: Append to valued hands so they are counted**
            if i % 2 == 0:
                if card_key != "back":
                    if player_card_multiplier > 1:
                        star_count = int((player_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
                        card_key = f"{'*' * star_count}{card_key}"  # Apply Multiplier (stars)
                        player_card_multiplier = 1 
                    if is_duality:
                        is_duality = False
                        card_key = f"-{card_key}"  # Apply Duality (negative sign)
                player_valued_hand.append(card_key)
            else:
                if card_key != "back":
                    if dealer_card_multiplier > 1:
                        star_count = int((dealer_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
                        card_key = f"{'*' * star_count}{card_key}"  # Apply Multiplier (stars)
                        dealer_card_multiplier = 1 
                    if is_duality_dealer:
                        is_duality_dealer = False
                        card_key = f"-{card_key}"  # Apply Duality (negative sign)
                dealer_valued_hand.append(card_key)

            draw_all_cards()
            pygame.display.flip()

    # Lock the first two cards in place
    locked_cards = 2
    new_card_positions = calculate_dynamic_positions(len(player_hand) - locked_cards)

    # Preserve initial positions for first two cards, update only new ones
    player_positions = player_positions[:locked_cards] + new_card_positions

    draw_value_boxes()
    if player_value == bust_value:
        hit_enabled = False
        stand_enabled = False
        flip_dealer_card()
        handle_dealer_logic()
        return
    if is_timestopped:
        is_timestopped = False
        hit_enabled = False
        stand_enabled = False
        flip_dealer_card()
        handle_dealer_logic()
    hit_enabled = True
    stand_enabled = True  # Enable hit button after first deal

################
#Deal New Cards#
################

# Animation -> Slide card if Joker and then flip the card
def reveal_joker(joker_type, target_pos, is_player=True, is_first_deal=False):
    global background, SIDEBAR_WIDTH
    global player_hand, dealer_hand, player_positions, card_positions, joker, player_valued_hand, dealer_valued_hand, is_duality, is_duality_dealer, dealer_card_multiplier, player_card_multiplier

    joker_image = card_images[f"Joker1"]
    middle_pos = ((SCREEN_WIDTH// 2) + 98, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2)
    slide_card(joker_image, (SCREEN_WIDTH, -200), middle_pos)

    if not joker:
        screen_shake(10, 600, joker_image, middle_pos)
        draw_joker_description(position="Reveal", joker_type=1)
        joker = True
        joker_type = 1
        pygame.time.delay(1200)

    pygame.time.delay(800)

    # Flip animation if not a normal joker
    if joker_type != 1:
        clock = pygame.time.Clock()
        steps = 500 // 24
        back_image = card_images[f"Joker{joker_type}"]

        for step in range(steps + 1):
            t = step / steps
            scale_factor = abs(1 - 2 * t)

            # Draw everything except the joker
            screen.blit(background, (0, 0))
            draw_value_boxes()
            draw_all_cards(exclude_last=False)

            if t < 0.5:
                # Shrinking joker
                scaled_joker = pygame.transform.scale(joker_image, (int(CARD_WIDTH * scale_factor), CARD_HEIGHT))
                screen.blit(scaled_joker, (middle_pos[0] + (CARD_WIDTH - scaled_joker.get_width()) // 2, middle_pos[1]))
            else:
                # Expanding back
                scaled_back = pygame.transform.scale(back_image, (int(CARD_WIDTH * scale_factor), CARD_HEIGHT))
                screen.blit(scaled_back, (middle_pos[0] + (CARD_WIDTH - scaled_back.get_width()) // 2, middle_pos[1]))

            pygame.display.flip()
            clock.tick(60)

        if joker_type in RARE_LIST:
            if joker_type == 65:
                if is_player:
                    player = True
                else:
                    player = False
                Null(is_player=player)

            screen_shake(10, 600, back_image, middle_pos)
            draw_joker_description(position="Reveal", joker_type=joker_type)
            pygame.time.wait(2000)
        else:
            draw_joker_description(position="Reveal", joker_type=joker_type)
            pygame.time.wait(2000)

    else:
        back_image = card_images["Joker1"]

    slide_card(back_image, middle_pos, target_pos)
    if is_player:
        player_hand.append(f"Joker{joker_type}")
        if joker_type == 1:
            joker_card_handler = "Joker1"
            if player_card_multiplier > 1:
                star_count = int((player_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
                joker_card_handler = f"{'*' * star_count}{joker_card_handler}"  # Apply Multiplier (stars)
                player_card_multiplier = 1 
            if is_duality:
                is_duality = False
                joker_card_handler = f"-{joker_card_handler}"  # Apply Duality (negative sign)
            player_valued_hand.append(joker_card_handler)
        else:
            if player_card_multiplier > 1:
                player_card_multiplier = 1 
            if is_duality:
                is_duality = False
        player_positions.append(target_pos)

        if joker_type == 43:
            Ascension(is_player=True)
        if is_first_deal:
            if joker_type == 44:
                DeadManHand(is_player=True)
        if joker_type == 45:
            Duality(is_player=True)
        if joker_type in [46, 47, 48, 49]:
            Multiplier(joker_type, is_player=True)
        if joker_type == 33:
            Malice(is_player=True)
        if joker_type == 105:
            Cosmic(is_player=True)
        if joker_type == 50:
            Breakthrough(is_player=True)
        if joker_type == 66:
            Jackpot()
        if joker_type == 74:
            Infernal()
        if joker_type == 35:
            EBT(is_player=True)
        if joker_type == 11 or joker_type == 12:
            TheKing(is_player=True)
        if joker_type == 63:
            TheRuler(is_player=True)
        if joker_type == 104:
            TheOne(is_player=True)
        if joker_type == 120:
            GiftOfHeavens(is_player=True)
        if joker_type == 153:
            TheOneAboveAll(is_player=True)

    else:
        dealer_hand.append(f"Joker{joker_type}")
        if joker_type == 1:
            joker_card_handler = "Joker1"
            if dealer_card_multiplier > 1:
                star_count = int((dealer_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
                joker_card_handler = f"{'*' * star_count}{joker_card_handler}"  # Apply Multiplier (stars)
                dealer_card_multiplier = 1 
            if is_duality_dealer:
                is_duality_dealer = False
                joker_card_handler = f"-{joker_card_handler}"  # Apply Duality (negative sign)
            dealer_valued_hand.append(joker_card_handler)
        else:
            if dealer_card_multiplier > 1:
                dealer_card_multiplier = 1 
            if is_duality_dealer:
                is_duality_dealer = False
        if len(dealer_hand) > 1:
            card_positions["dealer"].append(target_pos)

        if joker_type == 43:
            Ascension(is_player=False)
        if joker_type == 45:
            Duality(is_player=False)
        if joker_type in [46, 47, 48, 49]:
            Multiplier(joker_type, is_player=False)
        if joker_type == 33:
            Malice(is_player=False)
        if joker_type == 105:
            Cosmic(is_player=False)
        if joker_type == 50:
            Breakthrough(is_player=False)
        if joker_type == 35:
            EBT(is_player=False)
        if joker_type == 11 or joker_type == 12:
            TheKing(is_player=False)
        if joker_type == 63:
            TheRuler(is_player=False)
        if joker_type == 104:
            TheOne(is_player=False)
        if joker_type == 120:
            GiftOfHeavens(is_player=False)
        if joker_type == 153:
            TheOneAboveAll(is_player=False)
    draw_value_boxes()
    draw_all_cards()
    pygame.display.flip()

# Calculate positions to shift the previous cards
def calculate_dynamic_positions(num_cards):
    global SIDEBAR_WIDTH, SCREEN_WIDTH, CARD_WIDTH

    if num_cards == 0:
        return []

    max_width = (SCREEN_WIDTH - SIDEBAR_WIDTH)*0.7  # The max width that cards should cover
    available_space = max_width - CARD_WIDTH  # Ensure the first and last card don't exceed the boundary
    card_spacing = min(CARD_WIDTH + 10, available_space // max(1, num_cards - 1))  # Spacing
    playable_width = SCREEN_WIDTH - SIDEBAR_WIDTH

    total_width = card_spacing * (num_cards - 1) + CARD_WIDTH
    x_start = SIDEBAR_WIDTH + (playable_width - total_width) // 2  # Centered start position

    return [(x_start + i * card_spacing, SCREEN_HEIGHT - 80 - CARD_HEIGHT) for i in range(num_cards)]

# Animation -> Draw new card
def slide_card(card_image, start_pos, end_pos, duration=500):
    global background
    clock = pygame.time.Clock()
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    steps = duration // 24

    for i in range(steps + 1):
        t = i / steps
        x, y = int(start_x + t * (end_x - start_x)), int(start_y + t * (end_y - start_y))

        screen.blit(background, (0, 0))
        draw_all_cards()
        draw_value_boxes()
        screen.blit(card_image, (x, y))
        pygame.display.flip()
        clock.tick(60)

# Animation -> Move existing cards
def shift_cards_animation(old_positions, new_positions, duration=300):
    global background
    clock = pygame.time.Clock()
    steps = duration // 16

    for i in range(steps + 1):
        t = i / steps
        screen.blit(background, (0, 0))
        draw_value_boxes()
        # Change position
        for j, (old_pos, new_pos) in enumerate(zip(old_positions, new_positions)):
            x = int(old_pos[0] + t * (new_pos[0] - old_pos[0]))
            y = int(old_pos[1] + t * (new_pos[1] - old_pos[1]))
            screen.blit(card_images[player_hand[j]], (x, y))

        # Ensure the dealer's hand is drawn during every frame
        for k, card in enumerate(dealer_hand):
            if k < len(card_positions["dealer"]):
                x, y = card_positions["dealer"][k]
                screen.blit(card_images[card], (x, y))

        pygame.display.flip()
        clock.tick(60)

# Draw existing cards
def draw_all_except_revealed(exclude_index):
    global background
    screen.blit(background, (0, 0))
    draw_value_boxes()

    # Draw dealer's cards
    for i, card in enumerate(dealer_hand):
        if i == exclude_index:  # Skip the excluded card (Back)
            continue
        if i < len(card_positions["dealer"]):
            x, y = card_positions["dealer"][i]
            screen.blit(card_images[card], (x, y))

    # Draw player's cards
    for i, card in enumerate(player_hand):
        if i < len(player_positions):
            x, y = player_positions[i]
            screen.blit(card_images[card], (x, y))

# Draw all cards on screen
def draw_all_cards(exclude_last=False):
    global background
    screen.blit(background, (0, 0))
    draw_value_boxes()

    # Draw dealer's cards
    for i, card in enumerate(dealer_hand):
        if i < len(card_positions["dealer"]):
            x, y = card_positions["dealer"][i]
            screen.blit(card_images[card], (x, y))

    # Draw player's cards
    for i, card in enumerate(player_hand):
        if exclude_last and i == len(player_hand) - 1:
            continue
        if i < len(player_positions):
            x, y = player_positions[i]
            screen.blit(card_images[card], (x, y))

    draw_value_boxes()

# Calculate new card position
def deal_new_card():
    global background, SIDEBAR_WIDTH, status
    global player_positions, hit_enabled, stand_enabled, joker, number_of_hits, ascension, bust_value, is_duality, player_card_multiplier, is_infernal, money_amount, bet, money_multiplier

    if len(deck) == 0:
        return

    card = deck.pop()
    start_pos = (SCREEN_WIDTH, -200)  # Ensure new cards always start from here

    if card == "Joker":
        joker_type = determine_joker_type()
        target_pos = calculate_dynamic_positions(len(player_hand) + 1)[-1]
        reveal_joker(joker_type, target_pos, is_player=True)
    else:
        luck_chance = random.randint(1,100)
        if luck_chance < 5:
            card_image = card_images[f"gold{card}"]
            player_hand.append(f"gold{card}")
            money_multiplier += 0.3
        elif luck_chance < 10:
            card_image = card_images[f"steel{card}"]
            player_hand.append(f"steel{card}")
            money_multiplier += 0.1
        else:
            card_image = card_images[card]
            player_hand.append(card)
        card2 = card
        if player_card_multiplier > 1:
            star_count = int((round(player_card_multiplier) - 1) * 10)  # Example: 1.3x → 3 stars
            card2 = f"{'*' * star_count}{card2}"  # Apply Multiplier (stars)
            player_card_multiplier = 1 
        if is_duality:
            is_duality = False
            card2 = f"-{card2}"  # Apply Duality (negative sign)
        player_valued_hand.append(card2)  # **Fix: Append to valued_hand for calculation**

        new_card_pos = calculate_dynamic_positions(len(player_hand))[-1]
        slide_card(card_image, start_pos, new_card_pos)
        player_positions.append(new_card_pos)

    old_positions = player_positions[:]
    player_positions = calculate_dynamic_positions(len(player_hand))
    shift_cards_animation(old_positions, player_positions)

    draw_all_cards()
    draw_buttons()

    if card == "Joker" and joker_type == 44:
        DeadManHand(is_player=True)

    # **Fix: Call update value function**
    draw_value_boxes()

    if ascension and number_of_hits == ascension_limit:
        hit_enabled = False  # Disable further hitting
        stand_enabled = False
        flip_dealer_card()
        handle_dealer_logic()  # Transition to dealer’s turn
        return  # Exit immediately, do not reset bust_value here!

    if player_value > bust_value and not ascension:
        stand_enabled = False
        status = "Dealer wins!"
        if is_infernal:
            money_amount -= int(bet*3)
        else:
            money_amount -= bet
        draw_value_boxes()
        return

    if player_value == bust_value and not ascension:
        stand_enabled = False
        hit_enabled = False
        flip_dealer_card()
        handle_dealer_logic()
        return

    hit_enabled = True
    pygame.display.flip()

################
#Visual Effects#
################

def screen_shake(intensity=5, duration=500, joker_image=None, joker_pos=None):
    global background
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < duration:
        # Generate random screen offsets
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)

        # Clear the screen
        screen.blit(background, (0, 0))
        draw_value_boxes()

        # Redraw all cards with the shake offset
        for i, card in enumerate(dealer_hand):
            if i < len(card_positions["dealer"]):
                x, y = card_positions["dealer"][i]
                screen.blit(card_images[card], (x + offset_x, y + offset_y))

        for i, card in enumerate(player_hand):
            if i < len(player_positions):
                x, y = player_positions[i]
                screen.blit(card_images[card], (x + offset_x, y + offset_y))

        # Ensure the Joker remains visible in the middle
        if joker_image and joker_pos:
            x, y = joker_pos
            screen.blit(joker_image, (x + offset_x, y + offset_y))

        pygame.display.update()
        clock.tick(60)  # Smooth animation

    draw_all_cards()
    if joker_image and joker_pos:
        screen.blit(joker_image, joker_pos)  # Ensure Joker remains visible after shake
    pygame.display.update()

###############
#Joker Effects#
###############

def Ascension(is_player=True):
    global ascension, ascension_dealer, number_of_hits, ascension_limit, bust_value, dealer_bust_value

    if is_player:
        ascension = True
        number_of_hits = 0  # Reset hit count
    else:
        ascension_dealer = True
    if is_player:
        bust_value = float("inf")  # Remove bust limit for player
    else:
        dealer_bust_value = float("inf")

def DeadManHand(is_player=True):
    global player_value, dealer_value, money_amount, is_infernal, bet, money_multiplier
    global status

    if is_player:
        update_player_value()
        player_value *= 3  # Multiply player's hand value by 3
        if player_value > bust_value:
            status = "Dealer wins!"
            if is_infernal:
                money_amount -= int(bet*3)
            else:
                money_amount -= bet
            draw_value_boxes()
    else:
        update_dealer_value()
        dealer_value *= 3  # Multiply dealer's hand value by 3
        if dealer_value > dealer_bust_value:
            status = "You win!"
            if is_infernal:
                money_multiplier += 1
            money_amount += int(bet*money_multiplier)
            draw_value_boxes()

def Duality(is_player=True):
    global is_duality, is_duality_dealer

    if is_player:
        is_duality = True  # Player's next card will subtract
    else:
        is_duality_dealer = True  # Dealer's next card will subtract

def Multiplier(joker_type, is_player=True):
    global player_card_multiplier, dealer_card_multiplier

    # Define the multipliers based on the joker type
    multipliers = {
        46: 1.2,
        47: 1.3,
        48: 1.4,
        49: 1.5
    }

    if joker_type in multipliers:
        multiplier = multipliers[joker_type]

        if is_player:
            player_card_multiplier = multiplier  # Apply to player
        else:
            dealer_card_multiplier = multiplier

def Jackpot():
    global money_multiplier
    money_multiplier += 0.5

def Malice(is_player=True):
    global bust_value, dealer_bust_value
    if is_player:
        dealer_bust_value -= 5
    else:
        bust_value -= 5

def Infernal():
    global is_infernal
    is_infernal = True

def Cosmic(is_player=True):
    global player_value_multiplier, dealer_value_multiplier
    if is_player:
        player_value_multiplier += 0.2
    else:
        dealer_value_multiplier += 0.2

def EBT(is_player=True):
    global is_timestopped, is_timestopped_dealer
    if is_player:
        is_timestopped_dealer = True
    else:
        is_timestopped = True

def Breakthrough(is_player=True):
    global bust_value, dealer_bust_value
    if is_player:
        bust_value += 5
    else:
        dealer_bust_value += 5

def Null(is_player=True):
    global player_value, dealer_value, player_hand, dealer_hand, card_images, bet, money_amount, money_multiplier, is_infernal, status

    if is_player:
        # Change only the images of the existing cards to "Null"
        for i in range(len(player_hand)):
            player_hand[i] = "Null"

        update_player_value()
        player_value = randint(1, (bust_value if not ascension else 50))
        if player_value > bust_value:
            status = "Dealer wins!"
            if is_infernal:
                money_amount -= int(bet*3)
            else:
                money_amount -= bet
            draw_value_boxes()
    else:
        # Change only the images of the existing cards to "Null"
        for i in range(len(dealer_hand)):
            dealer_hand[i] = "Null"

        update_dealer_value()
        dealer_value = randint(1, (dealer_bust_value if not ascension_dealer else 50))
        if dealer_value > dealer_bust_value:
            status = "You win!"
            if is_infernal:
                money_multiplier += 1
            money_amount += int(bet*money_multiplier)
            draw_value_boxes()

    # **Update the display to reflect the changes**
    draw_all_cards()
    pygame.display.flip()

def TheOneAboveAll(is_player=True):
    global dealer_value, player_value, dealer_bust_value, bust_value
    if is_player:
        player_value = bust_value
    else:
        dealer_value = dealer_bust_value

def TheKing(is_player=True):
    global dealer_value, player_value
    if is_player:
        player_value += 11
    else:
        dealer_value += 11

def TheRuler(is_player=True):
    global dealer_value, player_value
    if is_player:
        player_value += 13
    else:
        dealer_value += 13

def TheOne(is_player=True):
    global dealer_value, player_value
    if is_player:
        player_value += 15
    else:
        dealer_value += 15

def GiftOfHeavens(is_player=True):
    global dealer_value, player_value
    global player_value_multiplier, dealer_value_multiplier

    cur_deal_val = dealer_value
    cur_play_val = player_value

    if is_player:
        player_value_multiplier += 0.5
    else:
        dealer_value_multiplier += 0.5

    if is_player and player_value<dealer_value:
        player_value = cur_deal_val
        dealer_value = cur_play_val
    elif not is_player and dealer_value<player_value:
        player_value = cur_deal_val
        dealer_value = cur_play_val

#####################
#Deal Dealer's Cards#
#####################

# Animation -> Shift previous cards
def shift_dealer_cards_animation(old_positions, new_positions, duration=300):
    global background
    clock = pygame.time.Clock()
    steps = duration // 16

    for i in range(steps + 1):
        t = i / steps
        screen.blit(background, (0, 0))
        draw_value_boxes()
        # Interpolate positions for all dealer's cards
        for j in range(len(new_positions)):
            if j < len(old_positions):  # Interpolate for existing cards
                old_pos = old_positions[j]
                new_pos = new_positions[j]
                x = int(old_pos[0] + t * (new_pos[0] - old_pos[0]))
                y = int(old_pos[1] + t * (new_pos[1] - old_pos[1]))
            else:  # If the card is new, move it from its current final position
                new_pos = new_positions[j]
                x, y = new_pos  # Draw it in the new position as it's static during this animation

            # Draw the card at the interpolated or static position
            screen.blit(card_images[dealer_hand[j]], (x, y))

        # Draw player's cards during the animation
        for k, card in enumerate(player_hand):
            if k < len(player_positions):
                x, y = player_positions[k]
                screen.blit(card_images[card], (x, y))

        pygame.display.flip()
        clock.tick(60)

# Draw existing cards
def draw_all_except_dealer_new():
    global background
    screen.blit(background, (0, 0))
    draw_value_boxes()

    # Draw dealer's cards except the last one
    for i, card in enumerate(dealer_hand[:-1]):  # Skip the newest card
        if i < len(card_positions["dealer"]):
            x, y = card_positions["dealer"][i]
            screen.blit(card_images[card], (x, y))

    # Draw player's cards
    for i, card in enumerate(player_hand):
        if i < len(player_positions):
            x, y = player_positions[i]
            screen.blit(card_images[card], (x, y))

# Calculate positions
def calculate_dealer_positions(num_cards):
    global background
    if num_cards == 0:
        return []

    max_width = (SCREEN_WIDTH - SIDEBAR_WIDTH)*0.7  # The max width that cards should cover
    available_space = max_width - CARD_WIDTH  # Ensure the first and last card don't exceed the boundary
    card_spacing = min(CARD_WIDTH + 10, available_space // max(1, num_cards - 1))
    playable_width = SCREEN_WIDTH - SIDEBAR_WIDTH

    total_width = card_spacing * (num_cards - 1) + CARD_WIDTH
    x_start = SIDEBAR_WIDTH + (playable_width - total_width) // 2

    return [(x_start + i * card_spacing, 75) for i in range(num_cards)]

# Animation -> Draw new card
def dealer_draw_new_card():
    global background
    global card_positions, dealer_valued_hand, is_duality_dealer, dealer_card_multiplier

    if len(deck) == 0:
        return

    card = deck.pop()
    start_pos = (SCREEN_WIDTH // 2, -200)  # Ensure new cards always start from here

    if card == "Joker":
        joker_type = determine_joker_type()
        target_pos = calculate_dealer_positions(len(dealer_hand) + 1)[-1]
        reveal_joker(joker_type, target_pos, is_player=False)

    else:
        dealer_hand.append(card)
        card2 = card
        if dealer_card_multiplier > 1:
            star_count = int((dealer_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
            card2 = f"{'*' * star_count}{card2}"  # Apply Multiplier (stars)
            dealer_card_multiplier = 1 
        if is_duality_dealer:
            is_duality_dealer = False
            card2 = f"-{card2}"  # Apply Duality (negative sign)
        dealer_valued_hand.append(card2)  # **Fix: Append to valued_hand for calculation**

        new_card_pos = calculate_dealer_positions(len(dealer_hand))[-1]
        card_image = card_images[card]
        slide_card(card_image, start_pos, new_card_pos)
        card_positions["dealer"].append(new_card_pos)

    draw_all_except_dealer_new()
    pygame.display.flip()

    old_positions = card_positions["dealer"][:]
    card_positions["dealer"] = calculate_dealer_positions(len(dealer_hand))
    shift_dealer_cards_animation(old_positions, card_positions["dealer"])
    draw_all_cards()
    if card == "Joker" and joker_type == 44:
        DeadManHand(is_player=False)
    # **Fix: Call update value function**
    draw_value_boxes()
    pygame.display.flip()

    pygame.time.delay(400)

# Animation -> Reveal dealer's card
def flip_dealer_card():
    global background
    global dealer_hand, deck, joker, RARE_LIST, is_duality_dealer, dealer_card_multiplier

    revealed_card = deck.pop()
    revealed_card2 = revealed_card
    if revealed_card != "Joker":
        revealed_card_image = card_images[revealed_card]
    else:
        if not joker:
            joker_type = 1
        else:
            joker_type = determine_joker_type()
        revealed_card_image = card_images[f"Joker{joker_type}"]
        revealed_card = f"Joker{joker_type}"

    # Replace the back card in the dealer's hand with the revealed card
    dealer_hand[1] = revealed_card
    revealed_card3 = revealed_card
    if dealer_card_multiplier > 1:
        star_count = int((dealer_card_multiplier - 1) * 10)  # Example: 1.3x → 3 stars
        revealed_card3 = f"{'*' * star_count}{revealed_card3}"  # Apply Multiplier (stars)
        dealer_card_multiplier = 1 
    if is_duality_dealer:
        is_duality_dealer = False
        revealed_card3 = f"-{revealed_card3}"  # Apply Duality (negative sign)
    dealer_valued_hand.append(revealed_card3)

    clock = pygame.time.Clock()
    steps = 500 // 24
    back_card_image = card_images["back"]

    # Get the position of the face-down card
    x, y = card_positions["dealer"][1]

    for step in range(steps + 1):
        t = step / steps
        scale_factor = abs(1 - 2 * t)

        # Draw everything except the dealer's second card
        draw_all_except_revealed(1)

        if t < 0.5:
            # Shrinking back card
            scaled_back = pygame.transform.scale(back_card_image, (int(CARD_WIDTH * scale_factor), CARD_HEIGHT))
            screen.blit(scaled_back, (x + (CARD_WIDTH - scaled_back.get_width()) // 2, y))
        else:
            # Expanding revealed card
            scaled_reveal = pygame.transform.scale(revealed_card_image, (int(CARD_WIDTH * scale_factor), CARD_HEIGHT))
            screen.blit(scaled_reveal, (x + (CARD_WIDTH - scaled_reveal.get_width()) // 2, y))

        pygame.display.flip()
        clock.tick(60)
    draw_value_boxes()
    if revealed_card2 == "Joker" and not joker:
        screen_shake(10, 600, revealed_card_image, (x, y))
        draw_joker_description(position="Flip", joker_type=1)
        joker = True
        joker_sound.play()
        joker_sound.set_volume(0.8)
        pygame.time.wait(2000)
    if revealed_card2 == "Joker" and joker_type in RARE_LIST:
        if revealed_card2 == "Joker" and joker_type == 65:
            Null(is_player=False)
        screen_shake(10, 600, revealed_card_image, (x, y))
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type != 1:
        draw_joker_description(position="Flip", joker_type=joker_type)
        joker_sound.play()
        joker_sound.set_volume(0.8)
        pygame.time.wait(2000)
    if revealed_card2 == "Joker" and joker_type == 43:
        Ascension(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 33:
        Malice(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 44:
        DeadManHand(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 45:
        Duality(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type in [46, 47, 48, 49]:
        Multiplier(joker_type, is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 105:
        Cosmic(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 50:
        Breakthrough(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and (joker_type == 11 or joker_type == 12):
        TheKing(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 63:
        TheRuler(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 104:
        TheOne(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 120:
        GiftOfHeavens(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    if revealed_card2 == "Joker" and joker_type == 153:
        TheOneAboveAll(is_player=False)
        joker_sound.play()
        joker_sound.set_volume(0.8)
    dealer_hand[1] = revealed_card  # Set the revealed card in the dealer's hand
    draw_all_cards()
    draw_value_boxes()
    pygame.display.flip()

    pygame.time.delay(400)

#######
#Media#
#######

def draw_joker_description(position, joker_type):
    """Displays and fades out the description of a special Joker with a transparent rounded box."""
    global joker
    font_path = r"Assets/BalatroFont.ttf"
    font = pygame.font.Font(font_path, 24)  # Increased font size for readability

    # Joker Descriptions
    joker_descriptions = {
        1: ("Joker", "+Random value"),
        11: ("The King", "+11 value"),
        12: ("The King", "+11 value"),
        63: ("The Ruler", "+13 value"),
        104: ("The One", "+15 value"),
        120: ("Gift of Heavens", "Switch hand and x1.5 hand value"),
        153: ("The One Above All", "Relic of The One"),
        43: ("Ascension", "Removes bust limit, but limit turn to 2"),
        44: ("Dead Man's Hand", "Multiplies current hand value by 3x"),
        45: ("Duality", "Next card subtracts value"),
        46: ("Multiplier", "Multiplies next card by 1.2x"),
        47: ("Multiplier", "Multiplies next card by 1.3x"),
        48: ("Multiplier", "Multiplies next card by 1.4x"),
        49: ("Multiplier", "Multiplies next card by 1.5x"),
        66: ("Jackpot", "Multiplies money earned by 1.5x"),
        33: ("Malice", "Opponent bust value -5"),
        74: ("Infernal", "2x money earned, lose 3x if lost"),
        105: ("Cosmic", "Multiplies final hand value by 1.2x"),
        35: ("Entity Beyond Time", "Relic of the God of Time"),
        50: ("Breakthrough", "Bust limit +5"),
        65: ("!#(@", "!#)@(!&$ !#!)& #!@*"),
    }

    if joker_type == 1 and joker:
        return  # Ignore if not a special Joker

    title, desc = joker_descriptions[joker_type]

    # Set default position if "Reveal"
    if position == "Reveal":
        x, y = 962, 670  # Default position where the Joker is revealed
    else:
        x, y = 1079, 360  # Use given position

    # Box properties
    box_width, box_height = 400, 80  # Adjusted size for readability
    border_radius = 12  # Rounded edges

    box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    box_surface.fill((0, 0, 0, 0))  # Clear previous framee
    pygame.draw.rect(box_surface, (30, 30, 30), (0, 0, box_width, box_height), border_radius=border_radius)

    # Render text with fading effect
    title_render = font.render(title, True, (255, 255, 255))
    desc_render = font.render(desc, True, (200, 200, 200))

    # Blit text onto the box surface
    box_surface.blit(title_render, (15, 10))  # Title at the top
    box_surface.blit(desc_render, (15, 45))  # Description below

    # Blit the box onto the main screen
    screen.blit(box_surface, (x, y))
    pygame.display.update()

# Draw cards
def draw_all_cards_without_values():
    """ Draws only cards without calling draw_value_boxes(). """
    global background

    # Redraw the background
    screen.blit(background, (0, 0))

    # Draw dealer's cards
    for i, card in enumerate(dealer_hand):
        if i < len(card_positions["dealer"]):
            x, y = card_positions["dealer"][i]
            screen.blit(card_images[card], (x, y))

    # Draw player's cards
    for i, card in enumerate(player_hand):
        if i < len(player_positions):
            x, y = player_positions[i]
            screen.blit(card_images[card], (x, y))

# Draw buttons
def draw_buttons():
    global hit_enabled, stand_enabled

    hit_button_img = pygame.image.load("Assets/HitButton.png").convert_alpha()
    hit_button_dark = pygame.image.load("Assets/HitButton dark.png").convert_alpha()
    stand_button_img = pygame.image.load("Assets/StandButton.png").convert_alpha()
    stand_button_dark = pygame.image.load("Assets/StandButton dark.png").convert_alpha()
    
    hit_button_dark = pygame.transform.scale(hit_button_dark, (BUTTON_WIDTH +30, BUTTON_HEIGHT +30))
    stand_button_dark = pygame.transform.scale(stand_button_dark, (BUTTON_WIDTH +30, BUTTON_HEIGHT +30))
    hit_button_img = pygame.transform.scale(hit_button_img, (BUTTON_WIDTH +30, BUTTON_HEIGHT +30))
    stand_button_img = pygame.transform.scale(stand_button_img, (BUTTON_WIDTH + 30, BUTTON_HEIGHT +30))

    if hit_button_rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hit_button_dark, hit_button_rect.topleft)
    else:
         screen.blit(hit_button_img, hit_button_rect.topleft)
    if stand_button_rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(stand_button_dark, stand_button_rect.topleft)
    else:
        screen.blit(stand_button_img, stand_button_rect.topleft)

   
    

# Hand Values
def draw_value_boxes():
    global player_value, dealer_value, bust_value, dealer_bust_value, player_value_multiplier, dealer_value_multiplier, is_duality, is_duality_dealer, player_card_multiplier, dealer_card_multiplier, ascension, ascension_dealer, deck
    global money_amount, bet, is_infernal, money_multiplier, roundnumber, status
    
    font_path = r"Assets/BalatroFont.ttf"
    font = pygame.font.Font(font_path, int(76*NEW_SCALER))
    round_font = pygame.font.Font(font_path, int(45*NEW_SCALER))

    # Text color
    text_color = (255, 255, 255)
    bet_color = (52, 255, 82)

    # Fonts
    money_font = pygame.font.Font(font_path, int(45*NEW_SCALER))
    bet_font = pygame.font.Font(font_path, int(54*NEW_SCALER))
    multi_font = pygame.font.Font(font_path, int(30*NEW_SCALER))
    deck_font = pygame.font.Font(font_path, int(45*NEW_SCALER))

    # Clear previous text by redrawing the background
    if status:
        screen.blit(background, (0, 0))
        draw_all_cards_without_values()
    
    update_dealer_value()
    update_player_value()

    # Box settings
    box_x_player, box_y_player = 35, 400
    box_x_dealer, box_y_dealer = 215, 400
    box_x_player_multi, box_y_player_multi = 35, 620
    box_x_dealer_multi, box_y_dealer_multi = 215, 620
    box_x_round, box_y_round = 310, 16
    box_x_money, box_y_money = 215, 707.5
    box_x_bet, box_y_bet = 70, 788
    box_x_multi, box_y_multi = 260, 802.5
    box_x_deck, box_y_deck = 1370, 13

    # Player text
    player_label = font.render(f"{player_value}", True, text_color)
    screen.blit(player_label, (box_x_player, box_y_player))

    player_label2 = font.render(f"{player_value_multiplier}x", True, text_color)
    screen.blit(player_label2, (box_x_player_multi, box_y_player_multi))

    # Dealer text
    dealer_label = font.render(f"{dealer_value}", True, text_color)
    screen.blit(dealer_label, (box_x_dealer, box_y_dealer))

    dealer_label2 = font.render(f"{dealer_value_multiplier}x", True, text_color)
    screen.blit(dealer_label2, (box_x_dealer_multi, box_y_dealer_multi))

    # Deck
    deck_label = deck_font.render(f"{len(deck)}", True, text_color)
    screen.blit(deck_label, (box_x_deck, box_y_deck))

    # Round
    round_label = round_font.render(f"{roundnumber}", True, text_color)
    screen.blit(round_label, (box_x_round, box_y_round))

    # Money
    money_label = money_font.render(f"{money_amount}", True, text_color)
    screen.blit(money_label, (box_x_money, box_y_money))

    money2_label = bet_font.render(f"{bet}", True, bet_color)
    screen.blit(money2_label, (box_x_bet, box_y_bet))

    money3_label = multi_font.render(f"{money_multiplier}x", True, text_color)
    screen.blit(money3_label, (box_x_multi, box_y_multi))

    # Status
    if status:
        if status == "Dealer wins!":
            status_font = pygame.font.Font(font_path, 35)
            box_x_status, box_y_status = 160, 150
            lose_sound.play()
            lose_sound.set_volume(0.8)
        elif status == "You win!":
            status_font = pygame.font.Font(font_path, 45)
            box_x_status, box_y_status = 160, 150
            win_sound.play()
            win_sound.set_volume(0.8)
        elif status == "Push!":
            status_font = pygame.font.Font(font_path, 55)
            box_x_status, box_y_status = 160, 140
        else:
            status_font = pygame.font.Font(font_path, 55)
            box_x_status, box_y_status = 160, 140

        status_label = status_font.render(status, True, text_color)
        screen.blit(status_label, (box_x_status, box_y_status))

        pygame.display.flip()  # Ensure the status is displayed before waiting
        pygame.time.wait(2000)  # Wait 2 seconds
        status = None
        reset_game()
    else:
        status_font = pygame.font.Font(font_path, 70)
        box_x_status, box_y_status = 160, 140

        status_label = status_font.render(f"{status}", True, text_color)
        screen.blit(status_label, (box_x_status, box_y_status))

###############
#Finish Screen#
###############

def reset_game():
    global background, roundnumber, dealer_aces, player_aces, bet, is_infernal
    global player_hand, dealer_hand, deck, player_positions, hit_enabled, stand_enabled, card_positions, card_images, player_valued_hand, dealer_valued_hand, ascension_dealer, number_of_hits, ascension, number_of_hits, bust_value, dealer_bust_value, player_value, dealer_value
    global dealer_breakthrough, player_breakthrough, money_multiplier, player_card_multiplier, dealer_card_multiplier, is_duality, is_duality_dealer,player_value_multiplier, dealer_value_multiplier, is_timestopped, is_timestopped_dealer
    player_hand = []
    dealer_hand = []
    player_valued_hand = []
    dealer_valued_hand = []
    player_value = 0
    dealer_value = 0
    player_positions = []
    hit_enabled = False
    stand_enabled = False
    ascension = False
    ascension_dealer = False
    number_of_hits = 0
    bust_value = 21
    dealer_bust_value = 21
    bust_value = 21
    dealer_breakthrough = False
    player_breakthrough = False
    player_card_multiplier = 1
    dealer_card_multiplier = 1
    is_duality = False
    is_duality_dealer = False
    player_value_multiplier = 1.0
    dealer_value_multiplier = 1.0
    is_timestopped = False
    is_timestopped_dealer = False
    dealer_aces = 0
    player_aces = 0
    roundnumber += 1
    bet = 100
    money_multiplier = 1.0
    is_infernal = False
    if len(deck) < 90:
        deck = generate_deck()
    card_positions = calculate_first_deal_positions()
    first_deal()

###################
#Value Calculation#
###################

# Return value
def get_card_value(card):
    global background
    is_negative = False
    star_count = 0
    if isinstance(card, str) and card.startswith("-"):
        is_negative = True
        card = card[1:]  # Remove negative sign before processing
    while card.startswith("*"):
        star_count += 1
        card = card[1:]
    if card == "Joker1":
        value = random.randint(1, 10)
    elif card[:2] == "Jo":
        value = 0
    elif card == "back":
        value = 0
    else:
        value = card[:-1]  # Strip suit
        if value in ["j", "q", "k"]:
            value = 10
        elif value == "a":
            value = 11  # Ace starts as 11, can adjust later
        else:
            value = int(value)
    multiplier = 1 + (star_count * 0.1)
    value *= multiplier
    shuffle_sound.play()
    shuffle_sound.set_volume(0.8)
    return -int(value) if is_negative else int(value)

# Update player's hand value
def update_player_value():
    global background, player_aces
    global player_value, player_valued_hand, bust_value
    while player_valued_hand:
        card = player_valued_hand.pop(0)  # Remove and process the first card in the list
        player_value += get_card_value(card)
        if card.startswith("a"):
            player_aces += 1
    while player_aces > 0 and player_value > bust_value:
        player_value -= 10
        player_aces -= 1
    
# Update dealer's hand value
def update_dealer_value():
    global background, dealer_aces
    global dealer_value, dealer_valued_hand, dealer_bust_value
    while dealer_valued_hand:
        card = dealer_valued_hand.pop(0)  # Remove and process the first card in the list
        dealer_value += get_card_value(card)
        if card.startswith("a"):
            dealer_aces += 1
        while dealer_aces > 0 and dealer_value > dealer_bust_value:
            dealer_value -= 10
            dealer_aces -= 1

# Blackjack logic
def handle_dealer_logic():
    global background, ascension_limit, is_timestopped_dealer, status, player_value_multiplier, dealer_value_multiplier
    global dealer_value, player_value, bust_value, dealer_bust_value, player_valued_hand, dealer_valued_hand, ascension_dealer, money_amount, money_multiplier, bet, is_infernal
    if not is_timestopped_dealer:
        if ascension_dealer:  # If dealer has Ascension, they draw exactly 2 more times
            for _ in range(2):
                dealer_draw_new_card()
                update_dealer_value()
                draw_value_boxes()

        else:
            if dealer_bust_value == 21:
                while dealer_value < 17:
                    dealer_draw_new_card()
                    update_dealer_value()
                    draw_value_boxes()
            else:
                while dealer_value < dealer_bust_value - 4:
                    dealer_draw_new_card()
                    update_dealer_value()
                    draw_value_boxes()
    else:
        is_timestopped_dealer = False
    
    # Final comparison and outcomes
    if player_value > bust_value and dealer_value > dealer_bust_value:
        if int(player_value*float(player_value_multiplier)) > int(dealer_value*float(dealer_value_multiplier)):
            status = "You win!"
            win_game = 1
        elif int(player_value*float(player_value_multiplier)) < int(dealer_value*float(dealer_value_multiplier)):
            status = "Dealer wins!"
            win_game = -1
        else:
            status = "Push!"
            win_game = 0
    elif player_value > bust_value:
        status = "Dealer wins!"
        win_game = -1
    elif dealer_value > dealer_bust_value or int(player_value*float(player_value_multiplier)) > int(dealer_value*float(dealer_value_multiplier)):
        status = "You win!"
        win_game = 1
    elif int(player_value*float(player_value_multiplier)) == int(dealer_value*float(dealer_value_multiplier)):
        status = "Push!"
        win_game = 0
    else:
        status = "Dealer wins!"
        win_game = -1
    
    if win_game == 1:
        if is_infernal:
            money_multiplier += 1
        money_amount += int(bet*money_multiplier)
    elif win_game == -1:
        if is_infernal:
            money_amount -= int(bet*3)
        else:
            money_amount -= bet
    
    draw_value_boxes()

    bet = 100
    money_multiplier = 1.0
    is_infernal = False

# Load assets
card_images = load_card_images()
deck = generate_deck()
card_positions = calculate_first_deal_positions()
player_positions = []

# Main
running = True
dealt = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == 0:
                game_active = 1
                start_sound.play()
                start_sound.set_volume(0.8)
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active == 1:
            if hit_enabled and hit_button_rect.collidepoint(event.pos):
                hit_enabled = False
                hit_sound.play()
                hit_sound.set_volume(0.8)
                if ascension:
                    number_of_hits += 1
                deal_new_card()
            elif stand_enabled and stand_button_rect.collidepoint(event.pos):
                hit_enabled = False
                stand_enabled = False
                stand_sound.play()
                stand_sound.set_volume(0.8)
                flip_dealer_card()
                handle_dealer_logic()
    
    if game_active == 1:
        if not dealt:
            first_deal()
            dealt = True

        screen.blit(background, (0, 0))
        draw_value_boxes()
        draw_all_cards()
        if hit_enabled or stand_enabled:
            draw_buttons()
        pygame.display.flip()
        win_lose()
    elif game_active == 0:
        start_game()

    pygame.display.update()
    clock.tick(60)
        
pygame.quit()