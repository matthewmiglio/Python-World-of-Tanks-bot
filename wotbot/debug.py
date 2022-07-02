import time

import numpy
import pydirectinput
from matplotlib import pyplot as plt
from wotbot.__main__ import restart_state

from wotbot.client import check_if_windows_exist
from wotbot.configuration import load_user_settings

from wotbot.logger import Logger
from wotbot.wot_main_screen import check_if_client_is_loading

logger = Logger()


# while True:
#     plt.imshow(numpy.asarray(screenshot()))
#     plt.show()

user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]
restart_state(launcher_path)