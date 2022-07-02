

import pydirectinput
import time
from wotbot.fight import check_team_status

from wotbot.wot_main_screen import check_for_apply_manageable_exp_button, check_for_battle_results_popup, check_for_tour_of_duty_popup, check_for_tribunal_popup, check_if_mission_completed_exists


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


def handle_mission_completed():
    if check_if_mission_completed_exists():
        pydirectinput.click(1827, 112, clicks=2, interval=0.2)


def handle_all_for_wot_main(logger):
    n=2
    while n!=0:
        handle_tour_of_duty_popup(logger)
        handle_battle_results_popups(logger)
        handle_tribunal_popup(logger)
        handle_manageable_exp(logger)
        handle_mission_completed()
        n=n-1 
    