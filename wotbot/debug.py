import time

import numpy
import pydirectinput
from matplotlib import pyplot as plt
from wotbot.__main__ import restart_state

from wotbot.client import check_if_windows_exist, screenshot
from wotbot.configuration import load_user_settings
from wotbot.fight import handle_last_alive

from wotbot.logger import Logger
from wotbot.wot_main_screen import check_if_client_is_loading, check_if_launcher_is_open, wait_for_launcher_to_open

logger = Logger()


# while True:
#     plt.imshow(numpy.asarray(screenshot()))
#     plt.show()

# user_settings = load_user_settings()
# launcher_path = user_settings["launcher_path"]
# restart_state(launcher_path)

# wait_for_launcher_to_open(logger)


handle_last_alive()