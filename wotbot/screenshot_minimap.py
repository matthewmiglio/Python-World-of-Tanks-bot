


import time
from fight import check_if_in_battle, screenshot_minimap


while True:
    if check_if_in_battle():
        screenshot_minimap()
        time.sleep(10)
    time.sleep(0.2)