import random
import time

import numpy
import pydirectinput
from matplotlib import pyplot as plt

from wotbot.client import check_quit_key_press, screenshot
from wotbot.image_rec import (check_for_location, find_references, get_avg_pix,
                              pixel_is_equal)
from wotbot.wot_main_screen import wait_for_wot_main


def screenshot_minimap():
    region = [1300, 485, 620, 595]
    ss = screenshot(region)
    t = time.localtime()
    path = r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\minimap_reference_screenshots"
    ss.save(f"{path}\\{t}.png")


def make_beginning_tank_moves():

    # once team passes, move uninterrupted for 10 sec to move away from flag to allow clean image detection
    # turn either left or right randomly then try to move
    n = random.randint(1, 2)
    s = random.randint(0, 2)
    if n == 1:
        pydirectinput.keyDown('a')
        time.sleep(s)
        pydirectinput.keyUp('a')
    if n == 2:
        pydirectinput.keyDown('d')
        time.sleep(s)
        pydirectinput.keyUp('d')
    pydirectinput.press('r')
    time.sleep(0.2)
    pydirectinput.press('r')
    time.sleep(0.2)
    pydirectinput.press('r')
    time.sleep(0.2)
    print("Moving away from flag")
# move away from flag
    time_spent_running = 0
    autorun()
    moving = check_if_moving()
    while time_spent_running < 3:
        while (moving) and (time_spent_running < 3):
            check_quit_key_press()
            time_spent_running = time_spent_running + 1
            print(time_spent_running)
            time.sleep(1)
            moving = check_if_moving()
        if time_spent_running < 3:
            check_quit_key_press()
            pydirectinput.keyDown('s')
            time.sleep(3)
            pydirectinput.keyUp('s')
            turn_randomly()
            autorun()
            time.sleep(2)
            moving = check_if_moving()
    print("Done making beginning moves.")
    pydirectinput.press('s')
    time.sleep(0.5)


def turn_randomly():
    n = 1
    s = random.randint(1, 3)
    pydirectinput.keyDown('s')
    time.sleep(2)
    pydirectinput.keyUp('s')
    if n == 1:
        pydirectinput.keyDown('a')
        time.sleep(s)
        pydirectinput.keyUp('a')


def autorun():
    pydirectinput.press('r')
    time.sleep(0.1)
    pydirectinput.press('r')
    time.sleep(0.1)
    pydirectinput.press('r')
    time.sleep(0.1)
    pydirectinput.press('r')
    time.sleep(0.1)


def check_if_waiting_for_battle():
    current_image = screenshot()
    reference_folder = "waiting_for_random_battle_logo"
    references = [
        "1.png",
        "2.png",
        "3.png",
    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)





def check_if_moving():
    moving = True
    count = 10
    while count > 0:
        moving = check_moving()
        if moving is False:
            return False
        time.sleep(0.15)
        count = count - 1
    return True


def check_moving():
    check_quit_key_press()
    region = [0, 600, 500, 500]
    current_image = screenshot(region=region)

    reference_folder = "1-5kmh"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        "6.png",
        "7.png",
        "8.png",
        "9.png",
        "10.png",
        "11.png",
        "12.png",
        "13.png",
        "14.png",
        "15.png",
        "16.png",
        "17.png",
        "18.png",
        "19.png",
        "20.png",
        "21.png",
        "22.png",
        "23.png",
        "24.png",
        "25.png",
        "26.png",
        "27.png",
        "28.png",
        "29.png",
        "30.png",
        "31.png",
        "32.png",
        "33.png",
        "34.png",
        "35.png",
        "36.png",
        "37.png",
        "38.png",
        "39.png",
        "40.png",
        "41.png",
        "42.png",
        "43.png",
        "44.png",
        "45.png",
        "46.png",
        "47.png",
        "48.png",
        "49.png",
        "50.png",
        "51.png",
        "52.png",
        "53.png",
        "54.png",
        "55.png",
        "56.png",
        "57.png",
        "58.png",
        "59.png",
        "60.png",
        "61.png",
        "62.png",
        "63.png",
        "64.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    output = check_for_location(locations)
    if output is True:
        return False
    if output is False:
        return True


def handle_tank_turning(current_direction, general_direction, logger):
    # if either params are empty for some reason turn randomly
    if (current_direction is None) or (general_direction is None):
        s = random.randint(0, 2)
        n = random.randint(1, 2)
        if n == 1:
            pydirectinput.keyDown('s')
            pydirectinput.keyDown('a')
            time.sleep(s)
            pydirectinput.keyUp('s')
            pydirectinput.keyUp('a')
            time.sleep(0.5)
        else:
            pydirectinput.keyDown('s')
            pydirectinput.keyDown('d')
            time.sleep(s)
            pydirectinput.keyUp('s')
            pydirectinput.keyUp('d')
            time.sleep(0.5)

    # if current direction returned stuck we 180
    if current_direction == "stuck":
        print("Tank stuck. Turning slightly.")
        pydirectinput.keyDown('s')
        time.sleep(2)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(2)
        pydirectinput.keyUp('a')
        return

# region turn_logic
    turn_to_make = ""
    cd = current_direction
    gd = general_direction

    # handle no turns
    if (cd == gd) and (cd is not None) and (gd is not None):
        turn_to_make = "No turn"

    # handle left turns
    if (cd == [1, 0, 0, 1]) and (gd == [1, 0, 1, 0]):
        turn_to_make = "left"
    if (cd == [0, 1, 0, 1]) and (gd == [1, 0, 0, 1]):
        turn_to_make = "left"
    if (cd == [1, 0, 0, 1]) and (gd == [0, 1, 1, 0]):
        turn_to_make = "left"
    if (cd == [0, 1, 1, 0]) and (gd == [0, 1, 0, 1]):
        turn_to_make = "left"

    # handle right turns
    if (cd == [0, 1, 1, 0]) and (gd == [1, 0, 1, 0]):
        turn_to_make = "right"
    if (cd == [1, 0, 1, 0]) and (gd == [1, 0, 0, 1]):
        turn_to_make = "right"
    if (cd == [0, 1, 0, 1]) and (gd == [0, 1, 1, 0]):
        turn_to_make = "right"
    if (cd == [1, 0, 0, 1]) and (gd == [0, 1, 0, 1]):
        turn_to_make = "right"

    # handle 180 turns
    if (cd == [0, 1, 0, 1]) and (gd == [1, 0, 1, 0]):
        turn_to_make = "180"
    if (cd == [0, 1, 1, 0]) and (gd == [1, 0, 0, 1]):
        turn_to_make = "180"
    if (cd == [1, 0, 0, 1]) and (gd == [0, 1, 1, 0]):
        turn_to_make = "180"
    if (cd == [1, 0, 1, 0]) and (gd == [0, 1, 0, 1]):
        turn_to_make = "180"

   # return turn_to_make
# endregion


# region make_turns
    # if no turns
    if turn_to_make == "No turn":
        logger.log("Making no turn.")
        return

    # if left turn
    if turn_to_make == "left":
        s = random.randint(1, 3)
        logger.log(f"Making left turn with duration of {s} seconds")
        pydirectinput.keyDown('s')
        time.sleep(1.3)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('a')
        time.sleep(s)
        pydirectinput.keyUp('a')

    # if right turn
    if turn_to_make == "right":
        s = random.randint(1, 3)
        logger.log(f"Making right turn with duration of {s} seconds")
        pydirectinput.keyDown('s')
        time.sleep(1.3)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(s)
        pydirectinput.keyUp('d')

    # if 180
    if turn_to_make == "180":
        s = 5.5
        logger.log(f"Making 180 turn using duration of {s} seconds")
        pydirectinput.keyDown('s')
        time.sleep(1.3)
        pydirectinput.keyUp('s')
        pydirectinput.keyDown('d')
        time.sleep(s)
        pydirectinput.keyUp('d')


# endregion


def check_team_status():
    team_status = [0] * 8

    region0 = [15, 98, 50, 20]
    region1 = [15, 123, 50, 20]
    region2 = [15, 149, 50, 20]
    region3 = [15, 175, 50, 20]
    region4 = [15, 199, 50, 20]
    region5 = [15, 224, 50, 20]
    region6 = [15, 248, 50, 20]
    region7 = [15, 275, 50, 20]

    region0_color = get_avg_pix(region0)
    region1_color = get_avg_pix(region1)
    region2_color = get_avg_pix(region2)
    region3_color = get_avg_pix(region3)
    region4_color = get_avg_pix(region4)
    region5_color = get_avg_pix(region5)
    region6_color = get_avg_pix(region6)
    region7_color = get_avg_pix(region7)

    sentinel = [50, 98, 26]

    if pixel_is_equal(region0_color, sentinel, tol=45):
        team_status[0] = 1
    if pixel_is_equal(region1_color, sentinel, tol=45):
        team_status[1] = 1
    if pixel_is_equal(region2_color, sentinel, tol=45):
        team_status[2] = 1
    if pixel_is_equal(region3_color, sentinel, tol=45):
        team_status[3] = 1
    if pixel_is_equal(region4_color, sentinel, tol=45):
        team_status[4] = 1
    if pixel_is_equal(region5_color, sentinel, tol=45):
        team_status[5] = 1
    if pixel_is_equal(region6_color, sentinel, tol=45):
        team_status[6] = 1
    if pixel_is_equal(region7_color, sentinel, tol=45):
        team_status[7] = 1

    teammates_alive = sum(team_status)

    # print(team_status)
    return teammates_alive


def move_turret_randomly():
    n = random.randint(1, 2)
    if n == 1:
        pydirectinput.keyDown('left')
        time.sleep(random.randint(1,4))
        pydirectinput.keyUp('left')
    if n == 2:
        pydirectinput.keyDown('right')
        time.sleep(random.randint(1,4))
        pydirectinput.keyUp('right')


def veer_left():
    check_quit_key_press()
    n = random.randint(1, 10)
    n = (n / 4.3)
    pydirectinput.keyDown('a')
    time.sleep(n)
    pydirectinput.keyUp('a')
    time.sleep(3)


def veer_right():
    check_quit_key_press()
    n = random.randint(1, 10)
    n = (n / 4.3)
    pydirectinput.keyDown('d')
    time.sleep(n)
    pydirectinput.keyUp('d')
    time.sleep(3)


def handle_last_alive(logger):
    if check_team_status() < 5:
        # if there only like 5 teammates left
        logger.log("Deserting because tank is like last alive.")
        time.sleep(1)
        pydirectinput.press('esc')
        time.sleep(1)
        pydirectinput.click(960, 542, clicks=3, interval=0.2)
        time.sleep(1)
        pydirectinput.moveTo(500, 500, duration=0.2)
        time.sleep(1)
        pydirectinput.click(1041, 751, clicks=6, interval=0.2)
        time.sleep(1)
        pydirectinput.moveTo(500, 500, duration=0.2)
        time.sleep(1)
        pydirectinput.click(1041, 751, clicks=6, interval=0.2)
        time.sleep(1)
        pydirectinput.moveTo(500, 500, duration=0.2)
        time.sleep(1)
        if wait_for_wot_main(logger) == "quit":
            return "quit"
        time.sleep(3)

        return "deserted"

