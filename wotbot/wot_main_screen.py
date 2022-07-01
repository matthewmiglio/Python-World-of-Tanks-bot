import os
import random
import time

import numpy
import pydirectinput
import pygetwindow
from cv2 import getWindowImageRect
from matplotlib import pyplot as plt

from wotbot.client import (check_quit_key_press, orientate_WOT_launcher,
                           screenshot, wait_for_start_WOT_buttom_to_be_orange)
from wotbot.image_rec import (check_for_location, coords_is_equal,
                              find_references, get_first_location,
                              pixel_is_equal)


def collect_manageable_exp_from_main():
    # open details menu
    get_to_details_menu()

    # loop a few times
    n = 0
    while n != 5:
        check_quit_key_press()
        # look for details buttons
        details_button_coords = find_details_button_in_details()
        # if we find a details button
        if details_button_coords is not None:
            # click detials button and open up battle report page
            pydirectinput.click(
                details_button_coords[0],
                details_button_coords[1],
                clicks=2,
                interval=0.2)
            # wait for page to load
            time.sleep(3)
            # look for apply button to apply manageable experience
            if check_for_apply_manageable_exp_button():
                pydirectinput.click(778, 574, clicks=2, interval=0.2)
                pydirectinput.moveTo(555, 555, duration=0.5)
                time.sleep(0.3)
            # after clicking apply button we gotta leave this page
            pydirectinput.click(1461, 209, clicks=2, interval=0.2)
            pydirectinput.moveTo(555, 555)

        # after completing a loop:

        # reopen details menu
        get_to_details_menu()

        # scroll amount of times that you looped
        time.sleep(2)
        times_to_scroll = n
        while times_to_scroll > 0:
            #print(f"Scrolling {times_to_scroll} times")
            scroll_up_in_details()
            time.sleep(0.2)
            times_to_scroll = times_to_scroll - 1

        # increment total loop
        n = n + 1

    # at the end click into space to close the details menu
    pydirectinput.click(555, 555)


def get_to_details_menu():
    check_quit_key_press()
    pydirectinput.click(1876, 1087, clicks=2, interval=0.2)
    pydirectinput.moveTo(555, 555)
    time.sleep(1)
    if not check_if_in_details_menu():
        get_to_details_menu()


def check_if_in_details_menu():
    current_image = screenshot()
    reference_folder = "details_menu"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def scroll_up_in_details():
    check_quit_key_press()
    button_coords = find_scroll_in_details()
    if button_coords is None:
        return "quit"

    amt_to_scroll = random.randint(20, 80)
    button_coords = [button_coords[1], button_coords[0]]
    destination_coords = [button_coords[0], button_coords[1] - amt_to_scroll]

    pydirectinput.mouseDown(
        x=button_coords[0],
        y=button_coords[1],
        button='left',
        duration=None)
    pydirectinput.moveTo(
        x=destination_coords[0],
        y=destination_coords[1],
        duration=1)
    pydirectinput.mouseDown(
        x=destination_coords[0],
        y=destination_coords[1],
        button='left',
        duration=None)
    pydirectinput.click(
        x=destination_coords[0],
        y=destination_coords[1],
        clicks=1)


def find_scroll_in_details():
    check_quit_key_press()
    current_image = screenshot()
    reference_folder = "details_scroll_button"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return get_first_location(locations)


def find_details_button_in_details():
    # get screenshot and est beginning loop vars
    iar = numpy.asarray(screenshot())
    x_coord = 1745
    y_coord = 584
    coord_list = []
    sentinel = [107, 107, 83]

    # loop through every pixel in range adding every coord that is EQ to
    # sentinel
    while y_coord < 1025:
        # get current pixel at coord
        coords = [x_coord, y_coord]
        current_pix = iar[y_coord][x_coord]

        # if pixel in range add it to list
        if pixel_is_equal(current_pix, sentinel, tol=10):
            if (coord_list == []):
                coord_list = [coords]
            else:
                coord_list.append(coords)

        # incremenet loop
        y_coord = y_coord + 1

    # print(coord_list)

    details_button_coords = verify_clusters_for_details(coord_list)
    if details_button_coords is not None:
        return details_button_coords
    return None


def verify_clusters_for_details(coord_list):
    # handle possibility of empty params
    if (coord_list is None):
        print("verify_clusters_for_details got called with empty params")
        return
    size = len(coord_list)
    if size == 0:
        print("verify_clusters_for_details got called with empty params")
        return

    # get loop vars
    top_index = size - 1
    inside_index = size - 1

    # loop
    while top_index > -1:
        # for each coord, look at the coords around it
        # coord in question:
        coord_in_question = coord_list[top_index]
        amt_of_coords_in_radius = 0

        while inside_index > -1:
            # compare the coord in question to each other coord and count the
            # number of similar coords.
            coord_to_compare_to = coord_list[inside_index]
            if coords_is_equal(coord_in_question, coord_to_compare_to, tol=10):
                amt_of_coords_in_radius = amt_of_coords_in_radius + 1
            if amt_of_coords_in_radius > 3:
                return coord_list[top_index]

            inside_index = inside_index - 1

        top_index = top_index - 1

    return None


def handle_manageable_exp(logger):
    if check_for_apply_manageable_exp_button():
        logger.log("Handling manageable exp")
        pydirectinput.click(778, 574, clicks=2, interval=0.2)
        pydirectinput.moveTo(555, 555, duration=0.5)
        time.sleep(0.3)


def check_for_apply_manageable_exp_button():
    current_image = screenshot()
    reference_folder = "manageable_exp_button"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def check_for_tour_of_duty_popup():
    current_image = screenshot()
    reference_folder = "tour_of_duty_popup"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def handle_tour_of_duty_popup(logger):
    if check_for_tour_of_duty_popup():
        logger.log("Handling tour of duty popup")
        pydirectinput.press('esc')
        time.sleep(0.2)


def wait_for_wot_main(logger):
    check_for_esc_menu()
    waiting = True
    if check_if_on_wot_main():
        waiting = False
    waiting_loops = 0
    while waiting:
        time.sleep(1)
        check_for_esc_menu()
        check_quit_key_press()
        handle_battle_results_popups(logger)
        handle_tribunal_popup(logger)

        waiting_loops = waiting_loops + 1
        logger.log(f"waiting for WOT main: {waiting_loops}")
        time.sleep(1)
        handle_mission_completed()
        if check_if_on_wot_main():
            waiting = False
        if waiting_loops > 100:
            logger.log("Waited too long for WOT main")
            return "quit"

    time.sleep(3)
    logger.log("Done waiting for WOT main.")
    time.sleep(3)
    


def check_for_esc_menu():
    n = 6
    while n != 0:
        current_image = screenshot()
        reference_folder = "wot_main_esc_menu"
        references = [
            "1.png",
            "2.png",
            "3.png",
            "4.png",
            "5.png",
            "6.png",
        ]

        locations = find_references(
            screenshot=current_image,
            folder=reference_folder,
            names=references,
            tolerance=0.97
        )
        exists = check_for_location(locations)
        if exists:
            pydirectinput.click(967, 797)
        n = n - 1
        time.sleep(0.2)


def restart_wot(logger, launcher_path):
    logger.log("Trying to close WoT window.")
    try:
        logger.log("Closing WoT window")
        WOT_client = pygetwindow.getWindowsWithTitle("WoT Client")[0]
        WOT_client.close()
        time.sleep(3)
    except BaseException:
        logger.log("Game is not already open. No matter.")

    logger.log("Opening WOT launcher.")
    wot_launcher_path = launcher_path
    os.system(wot_launcher_path)
    time.sleep(3)

    logger.log("Orientating WOT launcher")
    orientate_WOT_launcher()

    logger.log("Waiting for start.")
    wait_for_start_WOT_buttom_to_be_orange()

    logger.log("Opening WOT client")
    pydirectinput.click(150, 530)
    time.sleep(2)

    logger.log("Done restarting client. Waiting for main menu to appear.")
    if wait_for_wot_main(logger) == "quit":
        return "quit"


def handle_battle_results_popups(logger):

    handle_tour_of_duty_popup(logger)
    handle_tour_of_duty_popup(logger)
    handle_tour_of_duty_popup(logger)

    if check_for_battle_results_popup():
        logger.log("Handling battle results popup.")

        handle_tour_of_duty_popup(logger)

        handle_manageable_exp(logger)

        # clearing battle results popup page
        pydirectinput.click(1460, 211, clicks=2, interval=0.2)
        pydirectinput.moveTo(555, 555, duration=1)
        time.sleep(1)


def handle_tribunal_popup(logger):
    
    if check_for_tribunal_popup():
        logger.log("Handling tribunal popup.")
        # code to handle tribunal popup
        pydirectinput.click(1141, 797, clicks=3, interval=0.2)
        time.sleep(1)
        pydirectinput.moveTo(555, 555, duration=2)
        time.sleep(1)


def check_for_tribunal_popup():
    current_image = screenshot()
    reference_folder = "tribunal_popup"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def check_for_battle_results_popup():
    current_image = screenshot()
    reference_folder = "battle_results_popup"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def handle_mission_completed():
    if check_if_mission_completed_exists():
        pydirectinput.click(1827, 112, clicks=2, interval=0.2)


def check_if_mission_completed_exists():
    current_image = screenshot()
    reference_folder = "mission_completed_button"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def check_if_on_wot_main():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
    ]

    region = [12, 30, 70, 70]
    ss = screenshot(region)

    # iar=numpy.asanyarray(ss)
    # plt.imshow(iar)
    # plt.show()

    locations = find_references(
        screenshot=ss,
        folder="wot_main",
        names=references,
        tolerance=0.97
    )

    return check_for_location(locations)


def select_tank(logger, tank_prio):
    # click tank. if its available start battle
    slot_1_coords = [216, 900]
    slot_2_coords = [380, 900]
    slot_3_coords = [220, 1010]
    slot_4_coords = [380, 1010]

    # for each slot in tank prio:
    # find out which slot is in the current prio index
    # click it, then see if battle button appears. if it does, click start
    # battle and return.
    index = 0
    while index != 4:
        logger.log(f"Checking tank in priority {index}.")
        if tank_prio[index] == 1:
            logger.log("Checking tank in slot 1.")
            pydirectinput.click(
                slot_1_coords[0],
                slot_1_coords[1],
                clicks=3,
                interval=0.2)
            pydirectinput.moveTo(555, 555)
            if check_if_battle_button_exists():
                logger.log("Slot 1 tank is ready. Starting battle.")
                pydirectinput.click(960, 50, clicks=2, interval=0.2)
                return
        if tank_prio[index] == 2:
            logger.log("Checking tank in slot 2.")
            pydirectinput.click(
                slot_2_coords[0],
                slot_2_coords[1],
                clicks=3,
                interval=0.2)
            pydirectinput.moveTo(555, 555)
            if check_if_battle_button_exists():
                logger.log("Slot 2 tank is ready. Starting battle.")
                pydirectinput.click(960, 50, clicks=2, interval=0.2)
                return
        if tank_prio[index] == 3:
            logger.log("Checking tank in slot 3.")
            pydirectinput.click(
                slot_3_coords[0],
                slot_3_coords[1],
                clicks=3,
                interval=0.2)
            pydirectinput.moveTo(555, 555)
            if check_if_battle_button_exists():
                logger.log("Slot 3 tank is ready. Starting battle.")
                pydirectinput.click(960, 50, clicks=2, interval=0.2)
                return
        if tank_prio[index] == 4:
            logger.log("Checking tank in slot 4.")
            pydirectinput.click(
                slot_4_coords[0],
                slot_4_coords[1],
                clicks=3,
                interval=0.2)
            pydirectinput.moveTo(555, 555)
            if check_if_battle_button_exists():
                logger.log("Slot 4 tank is ready. Starting battle.")
                pydirectinput.click(960, 50, clicks=2, interval=0.2)
                return

        index = index + 1


def check_if_battle_button_exists():
    ss = numpy.asarray(screenshot())
    pix1 = ss[41][918]
    # print(pix1)
    sentinel = [230, 61, 14]
    if pixel_is_equal(pix1, sentinel, 40):
        return True
    return False
