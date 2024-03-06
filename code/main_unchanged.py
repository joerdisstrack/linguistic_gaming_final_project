### Linguistic Gaming with Python
### Names: Jisu Kim and Jördis Strack
### Matrikelnummer: 01/XXXXXXX and 01/919685

### NAME OF GAME AS IN GOOGLE DOC

# 0.1) load relevant libraries
import os
import pygame

# 0.2) set working directory for file and image-path to load background, characters and opponents
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

### 1) setup of stage

# 1.1) create frame and set dimensions

# first, initialize pygame object
pygame.init()

# set dimensions of frame - NOTE: CHANGE TO ADAPT TO DIFFERENT BACKGROUND
screen_width = 640
screen_height = 480

# create screen and display the screen to player
screen = pygame.display.set_mode((screen_width, screen_height))

# display caption of game:
pygame.display.set_caption("We had a nice name for this- GOOGLE DOCS")

# 1.2) Backdrop - change if possible
background = pygame.image.load(os.path.join(image_path, "background.png"))

### NOTE: DELETE potentially
# set stage/little walking board for character to stand on
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# set font and create game messages
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

game_result = "Game Over"

### 2) characters - NOTE: Here, we could enter several options with different speeds and weapons

# 2.1) create different characters
character = pygame.image.load(os.path.join(image_path, "character.png"))

# get size, width and height of character image
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]

# set initial position by placing player's character in middle of screen at the bottom
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# set change to new x-coordinate (to 0, since character has not moved yet)
character_to_x = 0

# set character speed
character_speed = 5


# 2.2) create balls - NOTE: Add some linguistic content here!
# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# initialize list containing different speedlevels for the balls # CHANGE!!!
ball_speed_y = [-18, -15, -12, -9]

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
    "init_spd_y": ball_speed_y[0]})

# finally, create status variables for balls, required for removal
ball_to_remove = -1


# 2.3) create characters weapons! - create some more!! And change them!!

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))

# set weapon dimensions
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# initialize empty list to contain all weapons that character shoots
weapons = []

# set speed of weapon when shot
weapon_speed = 10

# finally, create status variables for weapons, required for removal
weapon_to_remove = -1


# initiate clock object to measure time during game play
clock = pygame.time.Clock()


##### Start Gameplay

# set status of game to True, game has started
running = True

while running:
    dt = clock.tick(30)

    # for every event in pygame object check status and if it ends the game
    for event in pygame.event.get():
        # if yes, end game...
        if event.type == pygame.QUIT:
            # and set running-status to False...
            running = False

        # if any key is pressed, move character for as long as key is pressed down:
        # NOTE: Consider changing by how much we move
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

    # set initial weapon position to 0 (from above)
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
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:  # increase speed of ball slightly
            ball_val["to_y"] += 0.5

        # update ball coordinates
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # update character positioning
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    ### handle collisions between balls and character

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
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})

                    # and again for the second new ball, moving to the right
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,
                        # positive: right
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})

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
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    # draw walking board onto the screen
    screen.blit(stage, (0, screen_height - stage_height))
    # draw character onto the screen
    screen.blit(character, (character_x_pos, character_y_pos))

    # keep track of time by counting time that has passed
    # Note: the time module is very precise, divide by 1000 to obtain measures in seconds
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # set timer object and display time that is left, set True to display on screen, and colour code
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
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
msg = game_font.render(game_result, True, (255, 255, 0))

# create background for message to be displayed on
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)


# update screen so that player sees what's going on
pygame.display.update()

# leave final screen up for 5 seconds
pygame.time.delay(3000)

pygame.quit()
