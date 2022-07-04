

import pydirectinput
import time

from wotbot.client import screenshot
from wotbot.image_rec import check_for_location, find_references


def handle_tour_of_duty_popup(logger):
    if check_for_tour_of_duty_popup():
        logger.log("Handling tour of duty popup")
        pydirectinput.press('esc')
        time.sleep(0.2)


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
    #handle it twice i guess?
    n=2
    while n!=0:
        n=n-1
        #check if tribunal popup exists
        if check_for_tribunal_popup():
            logger.log("Handling tribunal popup.")
            # code to handle tribunal popup
            pydirectinput.click(1141, 797, clicks=3, interval=0.2)
            time.sleep(1)
            pydirectinput.moveTo(555, 555, duration=2)
            time.sleep(1)


def handle_manageable_exp(logger):
    if check_for_apply_manageable_exp_button():
        logger.log("Handling manageable exp")
        pydirectinput.click(778, 574, clicks=2, interval=0.2)
        pydirectinput.moveTo(555, 555, duration=0.5)
        time.sleep(0.3)


def handle_mission_completed(logger):
    if check_if_mission_completed_exists():
        logger.log("Handling mission completed")
        pydirectinput.click(1827, 112, clicks=2, interval=0.2)
        time.sleep(0.2)
        pydirectinput.moveTo(555,555)
        time.sleep(0.2)


def handle_all_for_wot_main(logger):
    n=2
    while n!=0:
        handle_tour_of_duty_popup(logger)
        handle_battle_results_popups(logger)
        handle_tribunal_popup(logger)
        handle_manageable_exp(logger)
        handle_mission_completed(logger)
        handle_credit_reserve_popup(logger)
        n=n-1 
    
    
def handle_credit_reserve_popup(logger):
    if check_for_credit_reserve_popup():
        logger.log("Handling credit reserve popup.")
        pydirectinput.click(965,781,clicks=3,interval=0.2)
        time.sleep(0.2)
        pydirectinput.moveTo(555,555)
        time.sleep(0.2)

    
def check_for_credit_reserve_popup():
    current_image = screenshot()
    reference_folder = "credit_reserve_popup"
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


