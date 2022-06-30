from os.path import dirname, join, exists
import json
import sys

top_level = dirname(__file__)
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
    if not exists(config_file):
        with open(config_file, "w") as f:
            default_config = {
                "tank_priority_stack": [1, 2, 3, 4]
            }
            f.write(json.dumps(default_config, indent=4))


create_config_file()
