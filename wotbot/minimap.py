from types import NoneType

import numpy
import PIL
from matplotlib import pyplot as plt
from PIL import Image

from wotbot.client import check_quit_key_press, screenshot
from wotbot.image_rec import (
    coords_is_equal,
    find_references,
    get_first_location,
    pixel_is_equal)


def determine_general_direction(myself_coords, enemy_flag_coords):
    # [up,down,left,right]

    # handle possible empty params
    if (myself_coords is None) or (enemy_flag_coords is None):
        print("Cannot determine a direction because either tank or enemy flag coords are missing.")
        return
    # determine directions
        # directions will be returned as an array denoting:
        # [up,down,left,right] as either trues or falses
    directions = [False] * 4

    if myself_coords[0] < enemy_flag_coords[0]:
        print("I should go right")
        directions[3] = True
    if myself_coords[0] > enemy_flag_coords[0]:
        print("I should go left")
        directions[2] = True
    if enemy_flag_coords[1] > myself_coords[1]:
        print("I should go down")
        directions[1] = True
    if enemy_flag_coords[1] < myself_coords[1]:
        print("I should go up")
        directions[0] = True
    if (not(directions[0])) and (not(directions[1])) and (
            not(directions[2])) and (not(directions[3])):
        return None
    return directions


def determine_current_direction(current_coords, prev_coords):
    # [up,down,left,right]

    # handle if params are empty

    if (current_coords is None) or (prev_coords is None):
        return None

    # if the coords are too similar that means you barely moved
    if coords_is_equal(current_coords, prev_coords, tol=15):
        print("Seems you barely moved. You should 180")
        return "stuck"

    # [up,down,left,right]
    directions = [False] * 4
    if prev_coords[0] > current_coords[0]:
        print("moving left")
        directions[2] = True
    if prev_coords[0] < current_coords[0]:
        print("moving right")
        directions[3] = True
    if current_coords[1] > prev_coords[1]:
        print("moving down")
        directions[1] = True
    if current_coords[1] < prev_coords[1]:
        print("moving up")
        directions[0] = True
    if (not(directions[0])) and (not(directions[1])) and (
            not(directions[2])) and (not(directions[3])):
        return None
    return directions


def find_myself_on_minimap():
    #print("Finding all white pixels")
    white_pix_list = find_white_pix_on_minimap()
    #print("Finding pixel that passes the test")
    if (white_pix_list is None) or (white_pix_list == []):
        #print("No white pixels found. Something is wrong.")
        return None
    size = len(white_pix_list) - 1
    while size > 0:

        pix_in_question_coords = white_pix_list[size]
        index_2 = len(white_pix_list) - 1
        total_surrounding_white_pix = 0
        while index_2 > 0:

            current_coords = white_pix_list[index_2]
            if coords_is_equal(pix_in_question_coords, current_coords, tol=5):
                total_surrounding_white_pix = total_surrounding_white_pix + 1
            index_2 = index_2 - 1
        if total_surrounding_white_pix > 45:
            # print("total_surrounding_white_pix",total_surrounding_white_pix)
            #print("Found myself")
            return pix_in_question_coords
        size = size - 1
    return None


def find_white_pix_on_minimap():
    #print("Starting to find white pixels")
    region = [1350, 530, 550, 550]
    ss = screenshot(region)

    # cycle through every pixel finding the white ones and their locations

    # ignore flag locations
    flags = find_team_flags_on_minimap()
    flag_1_coords = flags[0]
    flag_2_coords = flags[2]
    # handling when there are no flags for whatever reason
    if (flag_1_coords is None) or (flag_2_coords is None):
        #print("No flags found so I cant locate myself. Its just how it is.")
        return
    #print("Pasting images")
    # paste loc 1
    x = flag_1_coords[0]
    y = flag_1_coords[1]
    x = x - 50
    y = y - 50
    paste_loc_1 = [x, y]
    # paste loc 2
    x = flag_2_coords[0]
    y = flag_2_coords[1]
    x = x - 50
    y = y - 50
    paste_loc_2 = [x, y]
    # paste images over screenshot
    black = Image.open(
        r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black2.png")
    ss.paste(black, paste_loc_1)
    ss.paste(black, paste_loc_2)
    #print("Beginning loop")
    # looping throguh pixels
    ss = numpy.asarray(ss)
    # plt.imshow(ss)
    # plt.show()
    white_pix_list = []
    y_coord = 0
    sentinel = [225, 225, 225]
    while y_coord < 550:

        x_coord = 0
        while x_coord < 550:
            coords = [y_coord, x_coord]
            pix = ss[x_coord][y_coord]
            if pixel_is_equal(pix, sentinel, tol=35):
                white_pix_list.append(coords)
                # print(coords)
            x_coord = x_coord + 1

        y_coord = y_coord + 1
    # print(white_pix_list)
    # draw_picture(white_pix_list)
    #print("Done with loop. found all the white pixels")
    return white_pix_list


def draw_picture(coords):
    # make black image and open up white_pix image for pasting
    black_image = Image.open(
        r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black.png")
    white_pix = Image.open(
        r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\white_pix.png")
    image = screenshot(region=[0, 0, 550, 550])
    image.paste(black_image)

    # for each coord, paste a white pixel at each coord
    size = len(coords)

    print(size)
    print("-------")

    size = size - 1
    while size > 0:
        # print(size)

        image.paste(white_pix, coords[size])
        size = size - 1

    iar = numpy.asarray(image)
    plt.imshow(iar)
    plt.show()


def return_enemy_flag_coords(flags):
    # [flag1_coords,flag_1_side,flag2_coords,flag_2_side]
    if flags[1] == "enemy":
        return flags[0]
    if flags[3] == "enemy":
        return flags[2]


def find_team_flags_on_minimap():
    check_quit_key_press()
    # return vars
    flag1_coords = None
    flag2_coords = None
    flag_1_side = None
    flag_2_side = None

    # establish screenshot vars
    region = [1350, 530, 570, 550]
    screenshot_image = screenshot(region)

    # iar=numpy.asarray(screenshot_image)
    # plt.imshow(iar)
    # plt.show()

    # find first flag and identify it
    flag1_coords = look_for_flag_on_minimap(screenshot_image)
    if flag1_coords is not None:
        flag_1_side = identify_flag_side(flag1_coords)
        # cover first flag to avoid double-detection
        screenshot_image = cover_flag(flag1_coords, screenshot_image)

    # find another flag and identify it
    flag2_coords = look_for_flag_on_minimap(screenshot_image)
    if flag2_coords is not None:
        flag_2_side = identify_flag_side(flag2_coords)

    # assign which side is which
    if (flag_1_side is not None) and (flag_2_side is not None):
        if flag_1_side > flag_2_side:
            # meaning if flag1 has a higher amount of green pixels than flag2
            flag_1_side = "friendly"
            flag_2_side = "enemy"
        else:
            # meaning if flag2 has a higher amount of green pixels than flag1
            flag_1_side = "enemy"
            flag_2_side = "friendly"
    else:
        flag_1_side = "unk"
        flag_2_side = "unk"

    # print("flag1: ",flag1_coords,flag_1_side)
    # print("flag2: ",flag2_coords,flag_2_side)

    return [flag1_coords, flag_1_side, flag2_coords, flag_2_side]


def identify_flag_side(flag_coords):
    # returns a ratio of green to red pixels

    # if somehow this method got called with no coords to use we return
    if flag_coords is None:
        return

    # make flag_coords accurate
    flag_coords = [flag_coords[0] + 1350, flag_coords[1] + 530]

    # screenshot the minimap
    region = [flag_coords[0] - 20, flag_coords[1] - 20, 60, 60]
    ss = numpy.asarray(screenshot(region))

    # plt.imshow(ss)
    # plt.show()

    green_pix_total = 0
    red_pix_total = 0

    y_coord = 0
    while y_coord < 60:
        x_coord = 0
        while x_coord < 60:

            pix = ss[x_coord][y_coord]
            if not (pixel_is_equal(pix, [200, 200, 200], tol=50)):
                color = green_or_red(pix)
                if color == "red":
                    red_pix_total = red_pix_total + 1
                if color == "green":
                    green_pix_total = green_pix_total + 1
            x_coord = x_coord + 1
        y_coord = y_coord + 1

    if (green_pix_total == 0) or (red_pix_total == 0):
        return None
    return green_pix_total / red_pix_total


def green_or_red(pix):
    r = pix[0]
    g = pix[1]
    b = pix[2]
    if (r > g) and (r > b):
        return "red"
    if (g > r) and (g > b):
        return "green"
    return None


def look_for_flag_on_minimap(screenshot):

    # plt.imshow(screenshot)
    # plt.show()

    reference_folder = "minimap_friendly_flag"
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

    ]

    locations = find_references(
        screenshot=screenshot,
        folder=reference_folder,
        names=references,
        tolerance=0.99
    )
    coords = get_first_location(locations)
    if coords is None:
        return None
    return [coords[1], coords[0]]


def cover_flag(flag_coords, ss):
    # handle if this method got called with no params
    if (flag_coords is None) or (flag_coords == "unk"):
        return
    paste_image = Image.open(
        r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\paste_images\flag_cover.png")
    flag_coords = [flag_coords[0] - 50, flag_coords[1] - 50]
    ss.paste(paste_image, flag_coords)
    return ss
