### Linguistic Gaming with Python - Final Project

# WiSe 23/24
# Names: Jisu Kim and Jördis Strack
# Basic Inspiration for stage and setting: https://www.youtube.com/watch?v=Dkx8Pl6QKW0

import pygame
import sys
import os
import random

# first conveniently set paths
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# initialize pygame object
pygame.init()

# set window dimensions
menu_width = 640
menu_height = 480

# create screen and display the screen to player
menu_screen = pygame.display.set_mode((menu_width, menu_height))

# define menu captions
pygame.display.set_caption("Language Clash - Main Menu")

# set background for language clash
menu_background = pygame.image.load(os.path.join(image_path, "pencils_background.png"))

# set some basic non-colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set font
font = pygame.font.SysFont('arial', 32)

# define list of characters to choose from
characters = [
    pygame.image.load(os.path.join(image_path, "girl_character.png")),
    pygame.image.load(os.path.join(image_path, "boy_character.png")),
    pygame.image.load(os.path.join(image_path, "dino_character.png"))
]

# define list of weapons to choose from
weapons_images = [
    pygame.image.load(os.path.join(image_path, "weapon.png")),
    pygame.image.load(os.path.join(image_path, "pencil.png")),
    pygame.image.load(os.path.join(image_path, "bullet.png"))
]

# set different speeds for each character and weapon
character_speeds = [4, 5, 6]
weapon_speeds = [10, 15, 20]

# define function to conveniently draw text for the menu


def draw_text(text, font, color, surface, x, y):
    """
    :param text: text to be displayed
    :param font: set specific font
    :param color: define specific colour
    :param surface: screen/button over which text should be placed
    :param x: x-coordinate
    :param y: y-coordinate
    :return: text placed on object
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# let game start
def play():
    """
    function that creates a new pygame object to start the game
    :return: //
    """

    # 0.1) set working directory for file and image-path to load background, characters and opponents
    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, "images")

    # 0.2) setup of dictionary containing English, German and Korean vocabulary
    word_categories = {
        "Animal": {"English": "Animal", "German": "Tier", "Korean": "동물",
                   "German_words": ["Katze", "Hund", "Vogel", "Pferd", "Kuh"],
                   "Korean_words": ["고양이", "개", "새", "말", "암소"]},
        "School": {"English": "School", "German": "Schule", "Korean": "학교",
                   "German_words": ["Schüler", "Lehrer", "Klassenzimmer", "Tafel", "Semester"],
                   "Korean_words": ["학생", "교사", "교실", "칠판", "학기"]},
        "Job": {"English": "Job", "German": "Beruf", "Korean": "직장",
                "German_words": ["Lehrer", "Ärtzin", "Gärtner", "Friseur", "Köchin", "Pilotin"],
                "Korean_words": ["교사", "의사", "정원사", "미용실", "요리사", "비행사"]},
        "Food": {"English": "Food", "German": "Essen", "Korean": "음식",
                 "German_words": ["Nudeln", "Suppe", "Kimchi", "Kuchen"],
                 "Korean_words": ["파스타", "수프", "김치", "케이크"]},
        "Fruit": {"English": "Fruit", "German": "Obst", "Korean": "과일",
                  "German_words": ["Banane", "Apfel", "Erdbeere", "Lychee"],
                  "Korean_words": ["바나나", "사과", "딸기", "리치"]},
        "Vegetable": {"English": "Vegetable", "German": "Gemüse", "Korean": "채소",
                      "German_words": ["Karotte", "Kartoffel", "Zwiebel", "Knoblauch"],
                      "Korean_words": ["당근", "감자", "양파", "마늘"]}
    }

    # 0.2.1) choose a random word category
    selected_category = random.choice(list(word_categories.keys()))  # will serve as beginning of big ball

    # create lists used for word display on balls during game
    korean_words = word_categories[selected_category]["Korean_words"]
    german_words = word_categories[selected_category]["German_words"]
    word_list = [selected_category, word_categories[selected_category]["German"],
                 word_categories[selected_category]["Korean"],
                 german_words[0], korean_words[0], german_words[1], korean_words[1],
                 german_words[2], korean_words[2], german_words[3], korean_words[3]]

    # 1) setup of main stage

    # 1.1) create frame and set dimensions

    # first, initialize pygame object
    pygame.init()

    # set dimensions of frame
    screen_width = 640
    screen_height = 480

    # create screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    # set caption of game
    pygame.display.set_caption("Language Clash: Deutsch & 한국어 Edition")

    # 1.2) create background
    background = pygame.image.load(os.path.join(image_path, "background.png"))

    # set stage/little walking board for character to stand on
    stage = pygame.image.load(os.path.join(image_path, "stage.png"))
    stage_size = stage.get_rect().size
    stage_height = stage_size[1]

    # set font and create game messages
    game_font = pygame.font.SysFont('arial', 32)
    total_time = 100
    start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

    # set default game result in likely case of game over :)
    game_result = "Game Over"

    # 2) characters

    #  define function to set character selection screen
    def character_selection_screen():
        screen.fill((BLACK))
        selecting_character = True
        selected_character_index = None

        # display characters and instructions
        instructions = game_font.render("Press 1, 2, or 3 to select a character", True, (WHITE))
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, 20))

        # adjust character positions
        character_positions = [(screen_width // 4, screen_height // 2),
                               (screen_width // 2, screen_height // 2),
                               (3 * screen_width // 4, screen_height // 2)]

        for i, (char_img, position) in enumerate(zip(characters, character_positions)):
            char_rect = char_img.get_rect(center=position)
            screen.blit(char_img, char_rect)
            char_num = font.render(str(i + 1), True, (WHITE))
            screen.blit(char_num, (char_rect.centerx - char_num.get_width() // 2, char_rect.bottom + 10))

        pygame.display.update()

        # start loop for character selection
        while selecting_character:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_character_index = 0
                        selecting_character = False
                    elif event.key == pygame.K_2:
                        selected_character_index = 1
                        selecting_character = False
                    elif event.key == pygame.K_3:
                        selected_character_index = 2
                        selecting_character = False

        return selected_character_index

    # use character_selection_function to obtain index for character
    selected_character_index = character_selection_screen()

    # use character index to select a character
    character = characters[selected_character_index]

    # get character_speed
    character_speed = character_speeds[selected_character_index]

    # get size, width and height of character image
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]

    # set initial position by placing player's character in middle of screen at the bottom
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - character_height - stage_height

    # set change to new x-coordinate (to 0, since character has not moved yet)
    character_to_x = 0


    # 2.2) create balls
    ball_images = [
        pygame.image.load(os.path.join(image_path, "balloon1.png")),
        pygame.image.load(os.path.join(image_path, "balloon2.png")),
        pygame.image.load(os.path.join(image_path, "balloon3.png")),
        pygame.image.load(os.path.join(image_path, "balloon4.png"))]

    # initialize list containing different speed levels for the balls
    ball_speed_y = [-40, -35, -30, -25]

    # initialize empty list to store balls in
    balls = []

    # append the very first ball to the list of balls above
    balls.append({
        # x-coordinate
        "pos_x": 50,
        # y-coordinate
        "pos_y": 50,
        # image index of first ball
        "img_idx": 0,
        #  direction of x-axis movement, -3 to the left, 3 to the right
        "to_x": 3,
        # direction of y-axis movement, 6 spaces towards character
        "to_y": -6,
        # set initial speed of ball
        "init_spd_y": ball_speed_y[0],
        # word associated with this ball
        "word": word_list[0]
    })

    # finally, create status variables for balls, required for removal
    ball_to_remove = -1

    # 2.3) create characters weapons
    def weapon_selection_screen():
        screen.fill((BLACK))
        selecting_weapon = True
        selected_weapon_index = None

        # display weapons and instructions
        instructions = game_font.render("Press 1, 2, or 3 to select a weapon", True, (WHITE))
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, 20))

        # adjust weapon positioning
        weapon_positions = [(screen_width // 4, screen_height // 2),
                            (screen_width // 2, screen_height // 2),
                            (3 * screen_width // 4, screen_height // 2)]

        # readjust scaling
        scale_factor = 0.5

        for i, (weapon_img, position) in enumerate(zip(weapons_images, weapon_positions)):
            # scale the weapon image using scaling factor
            scaled_weapon_img = pygame.transform.scale(weapon_img, (
            int(weapon_img.get_width() * scale_factor), int(weapon_img.get_height() * scale_factor)))
            weapon_rect = scaled_weapon_img.get_rect(center=position)
            screen.blit(scaled_weapon_img, weapon_rect)
            weapon_num = game_font.render(str(i + 1), True, (BLACK))
            screen.blit(weapon_num, (weapon_rect.centerx - weapon_num.get_width() // 2, weapon_rect.bottom + 10))

        pygame.display.update()

        # start weapon selection loop
        while selecting_weapon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_weapon_index = 0
                        selecting_weapon = False
                    elif event.key == pygame.K_2:
                        selected_weapon_index = 1
                        selecting_weapon = False
                    elif event.key == pygame.K_3:
                        selected_weapon_index = 2
                        selecting_weapon = False

        return selected_weapon_index

    # call weapon_selection_screen after character_selection_screen
    selected_weapon_index = weapon_selection_screen()

    # use weapon index to set weapon
    weapon = weapons_images[selected_weapon_index]

    # set weapon dimensions
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]

    # initialize empty list to contain all weapons that character shoots
    weapons = []

    # set speed of weapon when shot
    weapon_speed = 10

    # finally, create status variables for weapons, required for removal
    weapon_to_remove = -1

    # initialize collision index to update displayed words
    collision_idx = 0

    # start gameplay

    # set status of game to True, game has started
    running = True

    # initiate clock object to measure time during game play
    clock = pygame.time.Clock()

    while running:

        dt = clock.tick(30)
        # for every event in pygame object check status and if it ends the game
        for event in pygame.event.get():
            # if yes, end game...
            if event.type == pygame.QUIT:
                # and set running-status to False...
                running = False

            # if any key is pressed, move character for as long as key is pressed down:
            if event.type == pygame.KEYDOWN:
                # move to left
                if event.key == pygame.K_LEFT:
                    character_to_x -= character_speed
                # move to right
                elif event.key == pygame.K_RIGHT:
                    character_to_x += character_speed
                # direct weapon - fire on space
                elif event.key == pygame.K_SPACE:
                    # initiate first weapon position, centered in the middle of character
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                    weapon_y_pos = character_y_pos
                    # append fired weapon to weapons list from above
                    weapons.append([weapon_x_pos, weapon_y_pos])

            # stop moving character as soon as key is not pressed down anymore
            if event.type == pygame.KEYUP:
                # this stops movement of character model on x-axis, NOT weapons - they can be fired without movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0

        # set initial character position to 0 (from above)
        character_x_pos += character_to_x

        # check if character movement does not violate frame guidelines
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # move weapons upwards to create 'shooting motion'
        weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

        # remove weapons that are out of frame guidelines
        weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

        # set ball positions
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # create 'bouncing motion' when balls hit any wall - horizontally
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1

            # create 'bouncing motion' when balls hit the top - vertically
            if ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] *= -1
            else:  # increase speed of ball slightly
                ball_val["to_y"] += 0.5

            # update ball coordinates
            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        # update character positioning
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        # handle collisions between balls and character

        # obtain ball-coordinates
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # update ball coordinates
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # check for ball and character collision
            if character_rect.colliderect(ball_rect):
                # if character model and ball collide, the game ends, status is set to False
                running = False
                break

            # update and obtain weapon coordinates
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_pos_x = weapon_val[0]
                weapon_pos_y = weapon_val[1]
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_pos_x
                weapon_rect.top = weapon_pos_y

                # check if ball and weapon collide - if yes, remove both the weapon and the ball!
                if weapon_rect.colliderect(ball_rect):
                    weapon_to_remove = weapon_idx
                    ball_to_remove = ball_idx
                    collision_idx += 1

                    # if ball is not of smallest size yet, split ball into two balls of next smaller size
                    if ball_img_idx < 3:
                        # change ball dimensions
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]
                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                        # append the two new smaller balls to ball-list, including coordinates and dimensions
                        # start with ball moving to the left
                        balls.append({
                            # x-coordinate
                            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            # y - coordinate
                            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            # set image index to be loaded
                            "img_idx": ball_img_idx + 1,
                            # direction of x-axis movement, negative: left
                            "to_x": -3,
                            # let ball move downwards toward character
                            "to_y": -6,
                            # set speed of ball based on size-index
                            "init_spd_y": ball_speed_y[ball_img_idx + 1],
                            "word": word_list[collision_idx % len(word_list)]
                        })

                        # and again for the second new ball, moving to the right
                        balls.append({
                            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            "img_idx": ball_img_idx + 1,
                            # positive: right
                            "to_x": 3,
                            "to_y": -6,
                            "init_spd_y": ball_speed_y[ball_img_idx + 1],
                            "word": word_list[(collision_idx + 1) % len(word_list)]
                        })

                    break
                # if there are still balls present and character has not collided with them, keep playing
            else:
                continue
            break  # if inner-for-loop is not satisfied, break both at once

        # remove balls and weapons that caused collision
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

        # if the player managed to shoot all balls, the game is won!
        if len(balls) == 0:
            # update game message to Success!
            game_result = "Congratulations, you won! Happy learning!!"
            # set status to False and end game
            running = False

        # draw all changes from above onto the screen
        screen.blit(background, (0, 0))

        # draw weapon shot onto screen
        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

        # draw all balls onto the screen
        for idx, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            word = val["word"]

            # project ball image onto screen
            screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

            # render and overlay associated word onto ball using a specified Korean font
            korean_font = pygame.font.Font("NotoSansCJKkr-Regular.otf", 20)
            word_text = korean_font.render(word, True, (WHITE))
            word_rect = word_text.get_rect(center=(ball_pos_x + ball_images[ball_img_idx].get_width() / 2,
                                                   ball_pos_y + ball_images[ball_img_idx].get_height() / 2))
            screen.blit(word_text, word_rect)

        # draw walking board onto the screen
        screen.blit(stage, (0, screen_height - stage_height))
        # draw character onto the screen
        screen.blit(character, (character_x_pos, character_y_pos))

        # keep track of time by counting time that has passed
        # Note: the time module is very precise, divide by 1000 to obtain measures in seconds
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        # set timer object and display time that is left, set True to display on screen, and colour code
        timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (BLACK))
        # draw timer to screen on top left
        screen.blit(timer, (10, 10))

        # should the player run out of time, they fail the game
        if total_time - elapsed_time <= 0:
            # change 'game result' to time over
            game_result = "Time Over"
            # set status to False, game has ended
            running = False

        pygame.display.update()

    # display result message to player after failing or completing the game (display=True), and colour code
    msg = game_font.render(game_result, True, (BLACK))

    # create background for message to be displayed on
    msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)

    # update screen so that player sees what's going on
    pygame.display.update()

    # leave final screen up for 2 seconds
    pygame.time.delay(2000)

    # fill screen with white color
    screen.fill((WHITE))

    # display main vocabulary topic once game has ended
    msg = game_font.render(selected_category, True, (BLACK))

    # create background for message to be displayed on
    msg_rect = msg.get_rect(center=(int(screen_width / 2), 20))
    screen.blit(msg, msg_rect)

    # calculate vertical spacing between each word pair [German & Korean]
    vertical_spacing = 40

    # calculate horizontal spacing between word pair [German & Korean]
    horizontal_spacing = 20

    # render and display all words from the word_list
    word_x_pos = int(screen_width / 4)  # start from left side of screen
    word_y_pos = msg_rect.bottom + 20  # Start below result message

    # define word pairs
    for i in range(1, len(word_list), 2):
        word1 = word_list[i]
        word2 = word_list[i + 1] if i + 1 < len(
            word_list) else ""  # handle case when there's an odd number of words

        # render the first word
        word1_text = korean_font.render(word1, True, (BLACK))
        word1_rect = word1_text.get_rect(topleft=(word_x_pos, word_y_pos))
        screen.blit(word1_text, word1_rect)

        # render the second word (if exists) next to the first word
        if word2:
            word2_text = korean_font.render(word2, True, (BLACK))
            word2_rect = word2_text.get_rect(topleft=(word1_rect.topright[0] + horizontal_spacing, word_y_pos))
            screen.blit(word2_text, word2_rect)

        # increment the vertical position for the next word pair
        word_y_pos = word1_rect.bottom + vertical_spacing

    # render and display final message below the last pair of words
    final_message = game_font.render("Take a screenshot of the words you learned!", True, (BLACK))
    final_message_rect = final_message.get_rect(midtop=(int(screen_width / 2), word_y_pos + 20))
    screen.blit(final_message, final_message_rect)

    # update screen so that player sees what's going on
    pygame.display.update()

    # leave final screen up for 5 seconds
    pygame.time.delay(5000)

    # return to main menu to allow for another play through
    main_menu()

    pygame.quit()


# see instructions


def instructions():
    """

    :return:
    """
    while True:
        menu_screen.blit(menu_background, (0, 0))
        draw_text('Instructions', font, BLACK, menu_screen, menu_width / 2, 100)

        # display instructions text
        instruction_text = [
            "Press left - move left",
            "Press right - move right",
            "Press space - fire weapon"]
        y_offset = 150
        for text in instruction_text:
            draw_text(text, font, BLACK, menu_screen, menu_width / 2, y_offset)
            y_offset += 30

        # back button
        mx, my = pygame.mouse.get_pos()
        button_back = pygame.Rect(menu_width / 2 - 100, 400, 200, 50)
        pygame.draw.rect(menu_screen, WHITE, button_back)
        draw_text('Return', font, BLACK, menu_screen, menu_width / 2, 425)

        if button_back.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                return  # return to main menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


# function to run main menu
def main_menu():
    while True:

        # blit predefined menu background
        menu_screen.blit(menu_background, (0, 0))
        # some other fun comment
        draw_text('Main Menu', font, BLACK, menu_screen, menu_width / 2, 100)

        mx, my = pygame.mouse.get_pos()

        button_start = pygame.Rect(menu_width / 2 - 100, 200, 200, 50)
        button_instructions = pygame.Rect(menu_width / 2 - 100, 270, 200, 50)
        button_exit = pygame.Rect(menu_width / 2 - 100, 340, 200, 50)

        pygame.draw.rect(menu_screen, WHITE, button_start)
        pygame.draw.rect(menu_screen, WHITE, button_instructions)
        pygame.draw.rect(menu_screen, WHITE, button_exit)

        draw_text('Play', font, BLACK, menu_screen, menu_width / 2, 225)
        draw_text('Instructions', font, BLACK, menu_screen, menu_width / 2, 295)
        draw_text('Exit', font, BLACK, menu_screen, menu_width / 2, 365)

        if button_start.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                play()
        if button_instructions.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                instructions()
        if button_exit.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main_menu()
