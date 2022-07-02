import time

import numpy
import pydirectinput
from matplotlib import pyplot as plt

from wotbot.client import check_if_windows_exist, screenshot
from wotbot.fight import check_if_in_battle
from wotbot.logger import Logger
from wotbot.wot_main_screen import check_for_tribunal_popup, wait_for_wot_main

logger = Logger()


# while True:
#     plt.imshow(numpy.asarray(screenshot()))
#     plt.show()

print(check_if_windows_exist(logger))
