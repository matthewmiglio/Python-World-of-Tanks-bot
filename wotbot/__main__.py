

import multiprocessing
import random
import sys
import time

import numpy
import pydirectinput
import pygetwindow
from matplotlib import pyplot as plt
from PIL import Image

from wotbot.client import check_quit_key_press, orientate_client
from wotbot.configuration import load_user_settings
from wotbot.fight import (autorun, check_if_dead, check_if_in_battle,
                          check_if_moving, check_if_waiting_for_battle,
                          move_turret_randomly, screenshot_minimap)
from wotbot.logger import Logger
from wotbot.wot_main_screen import (check_if_on_wot_main,
                                    collect_manageable_exp_from_main,
                                    handle_battle_results_popups,
                                    handle_manageable_exp,
                                    handle_mission_completed,
                                    handle_tour_of_duty_popup,
                                    handle_tribunal_popup, restart_wot,
                                    select_tank, wait_for_wot_main)

logger = Logger()


def detect_state(logger):
    handle_battle_results_popups(logger)
    handle_mission_completed()
    handle_tribunal_popup(logger)
    handle_tour_of_duty_popup(logger)

    if check_if_dead():
        logger.log("Detected tank is dead. Going to garage.")
        return "battle_over"
    if check_if_on_wot_main():
        logger.log("Detected WOT main")
        return "start"
    if check_if_in_battle():
        logger.log("Detected battle screen")
        return "random_battle_fight"
    logger.log("Found no states. Restarting")
    return "restart"


def start_state():
    check_quit_key_press()
    logger.log("-------STATE=START-------")
    # set battle mode
    logger.log("Setting battle mode to random battle")
    time.sleep(1)
    pydirectinput.click(1176, 62, clicks=3, interval=0.2)
    time.sleep(1)
    pydirectinput.click(468, 530, clicks=3, interval=0.2)
    time.sleep(3)
    # get to garage
    logger.log("clicking garage")
    time.sleep(2)
    pydirectinput.click(610, 98, clicks=3, interval=0.2)
    time.sleep(1)
    # set state to start_battle and return
    state = "start_battle"
    return state


def start_battle_state(tank_prio):
    if not(check_if_on_wot_main()):
        logger.log("start_battle_state got called while not on main.")
        return detect_state(logger)
    
    # handling various popups that may still be in the way on the WoT main
    # menu.
    handle_battle_results_popups(logger)
    handle_manageable_exp(logger)
    handle_mission_completed()
    handle_tribunal_popup(logger)
    handle_tour_of_duty_popup(logger)

    check_quit_key_press()
    logger.log("-------STATE=start_battle-------")
    # select da whip
    logger.log("Selecting tank")
    select_tank(logger, tank_prio)
    check_quit_key_press()

    # pydirectinput.click battle
    logger.log("Starting random battle")
    pydirectinput.click(960, 60, clicks=3, interval=0.2)
    check_quit_key_press()

    # add fight to logger
    logger.add_fight()
    check_quit_key_press()

    # wait for loading screen to start up or something. idk. bot flow gets
    # messed up without this pause.
    n = 10
    while n != 0:
        logger.log(f"Waiting: {n}")
        check_quit_key_press()

        time.sleep(1)
        n = n - 1

    # wait for battle to load
    waiting = True
    waiting_loops = 0
    while waiting:
        check_quit_key_press()
        waiting_loops = waiting_loops + 1
        waiting = check_if_waiting_for_battle()
        time.sleep(1)
        logger.log(f"Waiting for loading sequence: {waiting_loops}")
        time.sleep(1)

    # wait to let teammates pass us
    logger.log(
        "Waiting to let our teammates pass us.")
    n = 60
    while n > 0:
        check_quit_key_press()
        n = n - 1
        logger.log(f"Waiting...{n}")
        time.sleep(1)

    return "random_battle_fight"


def random_battle_fight_state(logger):
    check_quit_key_press()
    logger.log("-------STATE=random_battle_fight-------")
    check_quit_key_press()
    
    if not(check_if_in_battle()):
        logger.log("random_battle_fight_state got called while not in a battle.")
        return detect_state(logger)

    alive = not(check_if_dead())
    
    
    while alive:
        check_quit_key_press()

        # save screenshot of minimap for use for data in the future
        # logger.log("Screenshotting minimap for later use.")
        # screenshot_minimap()

        # start moving
        logger.log("Starting moving.")
        autorun()

        # make moving var
        moving = check_if_moving()
        time.sleep(1)

        # while moving do nothing
        while moving:
            check_quit_key_press()
            time.sleep(1)
            logger.log("Still moving. Sleeping")
            if not(check_if_moving()):
                moving = False

        logger.log("Moving is done.")
        pydirectinput.press('s')

        # move turret randomly just because
        move_turret_randomly()

        # turn left sometimes
        turn_duration = random.randint(1, 3)
        n = random.randint(1, 6)
        if n == 1:
            check_quit_key_press()
            logger.log("Turning left.")
            pydirectinput.keyDown('a')
            time.sleep(turn_duration)
            pydirectinput.keyUp('a')
        else:
            check_quit_key_press()
            logger.log("Turning right.")
            pydirectinput.keyDown('d')
            time.sleep(turn_duration)
            pydirectinput.keyUp('d')

        # alive checks

        logger.log("Dead check.")
        if check_if_dead():
            logger.log("Dead check confirmed dead.")
            alive = False
        if not (check_if_in_battle()):
            logger.log("Detected we're not in a battle.")
            return detect_state(logger)
        if check_if_on_wot_main():
            logger.log("Found we're on main somehow.")
            return "start"

    return "battle_over"


def battle_over_state():
    check_quit_key_press()
    logger.log("-------STATE=battle_over-------")
    logger.log("Going back to garage")
    # return to garage
    time.sleep(1)
    pydirectinput.press('esc')
    time.sleep(1)
    pydirectinput.click(956, 538, clicks=4, interval=0.2)
    check_quit_key_press()
    time.sleep(1)
    pydirectinput.moveTo(555, 555, duration=0.2)
    check_quit_key_press()
    time.sleep(1)
    pydirectinput.click(999, 623, clicks=4, interval=0.2)
    check_quit_key_press()
    time.sleep(1)
    pydirectinput.moveTo(555, 555, duration=0.2)
    check_quit_key_press()
    time.sleep(1)

    # wait for wot main to appear, and if this errors out pass to restart state
    logger.log("Waiting for WOT main")
    if wait_for_wot_main(logger) == "quit":
        return "restart"

    # if waiting was successful, wait an extra 5 sec then run the
    # collect_manageable_exp_from_main alg
    n = random.randint(1, 2)
    if n == 1:
        time.sleep(5)
        logger.log("Collecting manageable exp.")
        collect_manageable_exp_from_main()

    # pass to start state if things managed to get to this point
    return "start"


def restart_state(launcher_path):
    check_quit_key_press()
    orientate_client("WoT client", logger, resize=[1936, 1119])
    time.sleep(1)
    logger.add_fight()
    
    output=restart_wot(logger, launcher_path)
    
    if output == "quit":
        return "restart"
    if output == "random_battle_fight":
        return "random_battle_fight"
    
    return detect_state(logger)


def main():
    # user vars that will be changed through config file later
    user_settings = load_user_settings()
    tank_prio = user_settings["tank_priority_stack"]
    launcher_path = user_settings["launcher_path"]

    # main loop

    loops = 0
    orientate_client("WoT client", logger, resize=[1936, 1119])
    time.sleep(1)
    state = detect_state(logger)
    while True:
        loops = loops + 1
        logger.log(f"Loops: {loops}")
        if state == "restart":
            state = restart_state(launcher_path)
        if state == "start":
            state = start_state()
        if state == "start_battle":
            state = start_battle_state(tank_prio)
        if state == "random_battle_fight":
            state = random_battle_fight_state(logger)
        if state == "battle_over":
            state = battle_over_state()
        if state == "quit":
            sys.exit()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
