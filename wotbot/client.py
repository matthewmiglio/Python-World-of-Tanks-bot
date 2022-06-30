import os
import sys
import time

import keyboard
import numpy
import pyautogui
import pygetwindow
import pydirectinput

from image_rec import find_references, get_first_location, pixel_is_equal






def wait_for_start_WOT_buttom_to_be_orange():
    is_orange=check_if_start_WOT_buttom_is_orange()
    loops=0
    while not(is_orange):
        check_quit_key_press()
        loops=loops+1
        time.sleep(1)
        print(f"Waiting for start button: {loops}")
        is_orange=check_if_start_WOT_buttom_is_orange()
    
    
def check_if_start_WOT_buttom_is_orange():
    ss=screenshot()
    ss=numpy.asarray(ss)
    pix1=ss[534][104]
    pix2=ss[534][220]
    pix3=ss[538][104]
    
    # print(pix1)
    # print(pix2)
    # print(pix3)
    
    sentinel=[255,43,5]
    is_orange=False
    if (pixel_is_equal(pix1,sentinel,tol=45)):
        is_orange=True
    if (pixel_is_equal(pix2,sentinel,tol=45)):
        is_orange=True
    if (pixel_is_equal(pix3,sentinel,tol=45)):
        is_orange=True
    return is_orange


def orientate_WOT_launcher():
    launcher_window = pygetwindow.getWindowsWithTitle(
        "Wargaming.net Game Center")[0]
    launcher_window.minimize()
    launcher_window.restore()
    launcher_window.moveTo(0, 0)
    launcher_window.resizeTo(800, 600) # set size to 100x100


def orientate_client(title,logger,resize=None):
    try:
        client_window = pygetwindow.getWindowsWithTitle(
            title)[0]
        client_window.minimize()
        client_window.restore()
        client_window.moveTo(0, 0)
        if resize is not None:
            client_window.resizeTo(resize[0], resize[1])
    except: 
        logger.log("Could not find client.")
  

def check_if_windows_exist(logger):
    try:
        pygetwindow.getWindowsWithTitle('MEmu')[0]
        pygetwindow.getWindowsWithTitle('Multiple Instance Manager')[0]
    except (IndexError, KeyError):
        logger.log("MEmu or Multiple Instance Manager not detected!")
        return False
    return True


def check_if_on_memu_main():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        "6.png",

    ]
    locations = find_references(
        screenshot=refresh_screen(),
        folder="memu_main",
        names=references,
        tolerance=0.97
    )
    return get_first_location(locations)


def refresh_screen():
    check_quit_key_press()
    screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    check_quit_key_press()
    iar = numpy.array(screenshot)
    return iar


def screenshot(region=(0, 0, 1920, 1080)):
    if region is None:
        return pyautogui.screenshot()
    else:
        return pyautogui.screenshot(region=region)


def scroll_down():
    origin = pydirectinput.position()
    pydirectinput.moveTo(x=215, y=350)
    pydirectinput.dragTo(x=215, y=300, button='left', duration=1)
    pydirectinput.moveTo(x=origin[0], y=origin[1])


def scroll_up():
    origin = pydirectinput.position()
    pydirectinput.moveTo(x=215, y=300)
    pydirectinput.dragTo(x=215, y=350, button='left', duration=1)
    pydirectinput.moveTo(x=origin[0], y=origin[1])


def scroll_down_fast():
    origin = pydirectinput.position()
    pydirectinput.moveTo(x=215, y=350)
    pydirectinput.dragTo(x=215, y=300, button='left', duration=0.5)
    pydirectinput.moveTo(x=origin[0], y=origin[1])


def scroll_down_super_fast():
    origin = pydirectinput.position()
    pydirectinput.moveTo(x=215, y=400)
    pydirectinput.dragTo(x=215, y=300, button='left', duration=0.2)
    pydirectinput.moveTo(x=origin[0], y=origin[1])


def scroll_up_fast():
    origin = pydirectinput.position()
    pydirectinput.moveTo(x=215, y=300)
    pydirectinput.dragTo(x=215, y=350, button='left', duration=0.5)
    pydirectinput.moveTo(x=origin[0], y=origin[1])


def click(x, y, clicks=1, interval=0.0):
    original_pos = pydirectinput.position()
    loops = 0
    while loops < clicks:
        check_quit_key_press()
        pydirectinput.click(x=x, y=y)
        pydirectinput.moveTo(original_pos[0], original_pos[1])
        loops = loops + 1
        time.sleep(interval)


def check_quit_key_press():
    if keyboard.is_pressed("space"):
        print("Space is held. Quitting the program")
        sys.exit()
    if keyboard.is_pressed("pause"):
        print("Pausing program until pause is held again")
        time.sleep(2)
        pressed=False
        while not(pressed):
            time.sleep(0.05)
            if keyboard.is_pressed("pause"):
                print("Pause held again. Resuming program.")
                pressed=True 
