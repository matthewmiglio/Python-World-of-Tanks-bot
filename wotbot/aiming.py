


import random
import time
from operator import is_

import numpy
import pydirectinput
from matplotlib import pyplot as plt
from PIL import Image

from wotbot.client import check_quit_key_press, screenshot
from wotbot.image_rec import coords_is_equal, pixel_is_equal


def amt_to_aim_calculator(pix_to_move):
    #takes in pixels to move and returns a duration in seconds to use for turning camera
    return (pix_to_move*pix_to_move)/150000
    
    
def aim_at_enemy():
    check_quit_key_press()
    if check_if_has_shot()=="shot":
        return
    
    enemy_coords=find_enemy()  
    
    if (enemy_coords is None):
        return
    
    
    #true crosshair crosshair_location=[967,311]
    crosshair_coords=[967,261]
    

    x_offset=enemy_coords[0]-crosshair_coords[0]
    y_offset=enemy_coords[1]-crosshair_coords[1]
    
    if x_offset==0: x_offset=x_offset+1
    if y_offset==0: y_offset=y_offset+1
    
    duration_x=amt_to_aim_calculator(x_offset)
    duration_y=amt_to_aim_calculator(y_offset)

    direction_x="left"
    direction_y="up"

    if x_offset>0: direction_x="right"
    if x_offset<0: direction_x="left"
    if y_offset<0: direction_y="up"
    if y_offset>0: direction_y="down"
    
    # if abs(x_offset)<5: direction_x=None
    # if abs(y_offset)<5: direction_y=None
    
    # print("crosshair_coords ",crosshair_coords)
    # print("enemy_coords ",enemy_coords)
    
    # print("Horizontal| pix: ",x_offset, " direction: ",direction_x)
    # print("Vertical| pix: ",y_offset, " direction: ",direction_y)
    
    aim(direction_x=direction_x,direction_y=direction_y)
    
    if check_if_has_shot()=="shot":
        return
    
    
def aim(duration_x=0.001,duration_y=0.001,direction_x="left",direction_y="up"):
    #print(direction_x,direction_y)
    
    check_if_has_shot()
    
    if direction_x=="left":
        print("aiming left")
        pydirectinput.press('shift')
        pydirectinput.press('left')
        # pydirectinput.keyDown('left')
        # time.sleep(duration_x)
        # check_if_has_shot()
        # pydirectinput.keyUp('left')
        pydirectinput.press('shift')
        if check_if_has_shot()=="shot":
            return
    
    if direction_x=="right":
        print("aiming right")
        pydirectinput.press('shift')
        pydirectinput.press('right')
        # pydirectinput.keyDown('right')
        # time.sleep(duration_x)
        # check_if_has_shot()
        # pydirectinput.keyUp('right')
        pydirectinput.press('shift')
        if check_if_has_shot()=="shot":
            return
    if direction_y=="up":
        print("aiming up")
        pydirectinput.press('shift')
        pydirectinput.press('up')
        # pydirectinput.keyDown('up')
        # time.sleep(duration_y)
        # check_if_has_shot()
        # pydirectinput.keyUp('up')
        pydirectinput.press('shift')
        if check_if_has_shot()=="shot":
            return
    if direction_y=="down":
        print("aiming down")
        pydirectinput.press('shift')
        pydirectinput.press('down')
        # pydirectinput.keyDown('down')
        # time.sleep(duration_y)
        # check_if_has_shot()
        # pydirectinput.keyUp('down')
        pydirectinput.press('shift')
        if check_if_has_shot()=="shot":
            return
     
    
def draw_picture_for_aiming(coords,region):
    #make black image and open up white_pix image for pasting
    black_image=Image.open(r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black4.png")
    white_pix=Image.open(r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\white_pix.png")
    image=screenshot(region)
    paste_coords=[0,0]
    image.paste(im=black_image,box=paste_coords)
    
    #for each coord, paste a white pixel at each coord
    size=len(coords)
    if size==0:
        return
    
    #print(f"There were {size} red pixels found in the region.")
   
    
    size=size-1
    while size>0:
        #print(size)

        image.paste(white_pix,coords[size])
        size=size-1
    
    iar=numpy.asarray(image)
    plt.imshow(iar)
    plt.show()


def find_enemy():
    #get beginning image
    region=[0,178,1920,657]
    ss=screenshot(region)
    
    #doctor the photo to cover the minimap and the reload timer (which is sometimes red and may interfere with some detection idrk)
    reload_timer_cover_image=Image.open(r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black5.png")
    minimap_cover_image=Image.open(r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black6.png")
    enemy_player_count_image=Image.open(r"C:\Users\Matt\Desktop\1\my Programs\wot-bot\reference_images\draw_images\black7.png")
    
    reload_timer_coords=[801,335]
    minimap_coords=[1520,522]
    enemy_player_count_coords=[756,30]
    
    ss.paste(im=reload_timer_cover_image,box=reload_timer_coords)
    ss.paste(im=minimap_cover_image,box=minimap_coords)
    ss.paste(im=enemy_player_count_image,box=enemy_player_count_coords)
    
    # iar=numpy.asarray(ss)
    # plt.imshow(iar)
    # plt.show()
    
    
    #find coords of all red pixels in given image
    coords=find_red_pix_in_image(ss)
    
    #show the pixels that were found
    # draw_picture_for_aiming(coords,region)
    
    #using the coord list, return back any pixels that have a certain amount of other pixels around them.
    enemy_coords_list=find_enemy_given_red_image(coords)
    
    #using the next coord list, group up the coords and return consolidated estimated coordinates of enemy players.
    enemy_coords=consolidate_red_pix_into_coords(enemy_coords_list)

    #provided an enemy was found, look for the closest enemy to the crosshair
    closest_enemy_coords=find_enemy_coord_closest_to_crosshair(enemy_coords)

    #return that
    return closest_enemy_coords


def consolidate_red_pix_into_coords(enemy_coords_list):
    group_1=[]
    group_2=[]
    group_3=[]
    
    if (enemy_coords_list is None)or(len(enemy_coords_list)==0):
        return
    
    index=len(enemy_coords_list)
    
    while index>0:
        index=index-1
        #print(index)
        current_coords=enemy_coords_list[index]
        #check if group 1 is empty or if the coords fit in this group. add it
        if (group_1==[])or(coords_is_equal(current_coords,group_1[0],tol=15)): 
            group_1.append(current_coords)
            continue
        #check if group 2 is empty or if the coords fit in this group. add it
        if (group_2==[])or(coords_is_equal(current_coords,group_2[0],tol=15)): 
            group_2.append(current_coords)
            continue
        #check if group 3 is empty or if the coords fit in this group. add it
        if (group_3==[])or(coords_is_equal(current_coords,group_3[0],tol=15)): 
            group_3.append(current_coords)
            
    group_1_coords=get_average_coords(group_1)
    group_2_coords=get_average_coords(group_2)
    group_3_coords=get_average_coords(group_3)
    
    # print(group_1_coords)
    # print(group_2_coords)
    # print(group_3_coords)
    
    return [group_1_coords,group_2_coords,group_3_coords]
    
    
def get_average_coords(coords_list):
    index=len(coords_list)-1
    total_x=0
    total_y=0
    total_coords=0
    
    #handle none in params
    if (len(coords_list)==0)or(coords_list[0] is None):
        return
    
    while index>-1:
        total_x=total_x+coords_list[index][0]
        total_y=total_y+coords_list[index][1]
        total_coords=total_coords+1
        
        index=index-1

    avg_x=int(total_x/total_coords)
    avg_y=int(total_y/total_coords)
    
    return [avg_x,avg_y]


def find_enemy_given_red_image(coord_list):
    positive_case_coords_list=[]
    list1=coord_list
    list2=coord_list
    index_1=len(list1)-1
    
    if len(coord_list)==0:
        #print("Red pixel list is empty.")
        return None
    
    while index_1>-1:
    #for each coord in list 1
        #start from the top of list 2
        index_2=len(list2)-1
        #reset the pix in radius to zero bc new pixel
        pix_in_radius=0
        while index_2>-1:
        #for each coord in list 2
            #get each current coord
            #print(index_1)
            coords_1=coord_list[index_1]
            coords_2=coord_list[index_2]
            
            #if pixels are eq add 1 to counter
            if coords_is_equal(coords_1,coords_2,tol=45): pix_in_radius=pix_in_radius+1
            
            #check the counter. if its above whatever then its a positive case so we add to list of positive case coords
            if pix_in_radius>15:
                positive_case_coords_list.append(coords_1) 
            
            #incrementing
            index_2=index_2-1
        index_1=index_1-1
    
    #if we exit the loop without ever triggering the counter case we return None
    return positive_case_coords_list
  
    
def find_enemy_coord_closest_to_crosshair(coord_list):
    #handle if is none
    if (coord_list is None)or(len(coord_list)==0):
        #print("Coords list is empty so cant find closest enemy.")
        return
    
    crosshair_location=[967,311]
    index=len(coord_list)-1
    min_total_difference_value=None
    min_total_difference_coords=None
    while index>-1:
        #print(index)
        current_x=coord_list[index][0]
        current_y=coord_list[index][1]
        
        crosshair_x=crosshair_location[0]
        crosshair_y=crosshair_location[1]
        
        current_x_difference=abs(current_x - crosshair_x)
        current_y_difference=abs(current_y - crosshair_y)

        total_difference_value=(current_x_difference*current_x_difference)+(current_y_difference*current_y_difference)
        if (min_total_difference_value is None)or(min_total_difference_coords is None):
            min_total_difference_value=total_difference_value
            min_total_difference_coords=coord_list[index]
        if total_difference_value<min_total_difference_value:
            min_total_difference_value=total_difference_value
            min_total_difference_coords=coord_list[index]
            
        index=index-1
    
    return min_total_difference_coords


def find_red_pix_in_image(ss):
    iar=numpy.asarray(ss)
    height=iar.shape[0]-1
    width=iar.shape[1]-1
    red_pix_list=[]
    
    
    x_coord=0
    while x_coord<width:
        #print(f"X: {x_coord}")
        y_coord=0
        
        while y_coord<height:
        #for each pix
            #check if its red and if its red add its coord to the list.
            is_red=False
            pix=iar[y_coord][x_coord]
            #print(pix)
            
            coords=[x_coord,y_coord]
            sent1=[113,0,0]
            sent2=[139,2,1]
            sent3=[174,32,25]
            sent4=[231,12,0]
            sent5=[154,2,1]
            
            if pixel_is_equal(sent1,pix,tol=15): is_red=True
            if pixel_is_equal(sent2,pix,tol=15): is_red=True
            if pixel_is_equal(sent3,pix,tol=15): is_red=True
            if pixel_is_equal(sent4,pix,tol=15): is_red=True
            if pixel_is_equal(sent5,pix,tol=15): is_red=True
            
            
            if is_red:
                red_pix_list.append(coords)
        
            y_coord=y_coord+5
        x_coord=x_coord+5

    return red_pix_list


def check_if_has_shot():
    #screenshot region around crosshair
    region=[964,486,8,8]

    # ss=screenshot(region)
    # plt.imshow(numpy.asarray(ss))
    # plt.show()
    
    shot=scan_shot_region_for_shot(region)
    if (shot=="green")or(shot=="orange"):
        pydirectinput.click(clicks=10,interval=0.05)
        return "shot"
    if shot=="no shot":
        pass
        #print("No shot.")

    
def scan_shot_region_for_shot(region):
    ss=screenshot(region)
    iar=numpy.asarray(ss)
    x_coord=0
    while x_coord<region[2]:
        y_coord=0
        while y_coord<region[3]:
        #for each pixel:
            pix=iar[y_coord][x_coord]
            #if green 
            green_sent_1=[204,240,95]
            green_sent_2=[211,185,72]
            green_sent_3=[158,172,76]
            green_sent_4=[167,170,68]
            if pixel_is_equal(pix,green_sent_1,tol=15): 
                #print("G1")
                return "green"
            if pixel_is_equal(pix,green_sent_2,tol=15): 
                #print("G2")
                return "green"
            if pixel_is_equal(pix,green_sent_3,tol=15): 
                #print("G3")
                return "green"
            if pixel_is_equal(pix,green_sent_4,tol=15): 
                #print("G4")
                return "green"
            #if orange
            orange_sent_1=[250,119,0]
            #orange_sent_2=[207,113,27]
            orange_sent_3=[240,112,6]
            orange_sent_4=[243,121,7]
            orange_sent_5=[165,91,24]
            orange_sent_6=[199,89,1]
            if pixel_is_equal(pix,orange_sent_1,tol=15): 
                #print("O1")
                return "orange"
            if pixel_is_equal(pix,orange_sent_3,tol=15): 
                #print("O3")
                return "orange"
            if pixel_is_equal(pix,orange_sent_4,tol=15): 
                #print("O4")
                return "orange"
            if pixel_is_equal(pix,orange_sent_5,tol=15): 
                #print("O5")
                return "orange"
            if pixel_is_equal(pix,orange_sent_6,tol=15): 
                #print("O6")
                return "orange"
            
            
            
            y_coord=y_coord+1
        x_coord=x_coord+1
    return "no shot"


