import json
import sys
from os import makedirs
from os.path import exists, expandvars, isdir, join

top_level = join(expandvars(f'%appdata%'), "wot-bot")
config_file = join(top_level, 'config.json')


def load_user_settings():
    try:
        return json.load(open(config_file, 'r'))
    except json.JSONDecodeError:
        print("User config file could not be loaded, is it misconfigured?")
        sys.exit()
    except OSError:
        print("Could not find config file, creating one now")
        create_config_file()
        return load_user_settings()


def create_config_file():
    if not isdir(top_level):
        makedirs(top_level)
    if not exists(config_file):
        with open(config_file, "w") as f:
            default_config = {
                "tank_priority_stack": [
                    1,
                    2,
                    3,
                    4],
                "launcher_path": join(
                    "B:\\",
                    "Games",
                    "World_of_Tanks_NA",
                    "wgc_api.exe")}
            f.write(json.dumps(default_config, indent=4))


create_config_file()
