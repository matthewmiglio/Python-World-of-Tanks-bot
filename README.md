# World-of-Tanks-bot

[![Python Test](https://github.com/matthewmiglio/Python-World-of-Tanks-bot/actions/workflows/python-tests.yml/badge.svg)](https://github.com/matthewmiglio/Python-World-of-Tanks-bot/actions/workflows/python-tests.yml)

A World of Tanks automation bot written in Python.

## Install

[Download the latest release for Windows](https://github.com/matthewmiglio/Python-World-of-Tanks-bot).

### Configure client options

#### Graphics

    -display mode: Windowed
    -resolution: 1920x1020*
    -interface scaling: x1
    -color adjustment: 1940s cine film**
    -Use ctrl+ to maximize minimap once manually while in game 

    *if this resolution is all or most of your screen, taskbars placed on the sides or bottom of the screen may obstruct the bot.
    **color adjustment is theoretically unnecessary but image recognition problems may occur on varying color adjustment settings.


<br>

## Run World-of-Tanks-bot

Before attempting to run the bot, make sure both the World of Tanks client is open.

#### Installed on Windows

Run the desktop shortcut the installer created.

<br>

## Configuration

All configuration is through **`lib\pyclashbot\config.json`**,

#### Launcher Path

Define your launcher path as the absolute path to **`wgc_api.exe`**
Make sure to use double slash 

#### Tank Priority

1. Set only four primary tanks in the garage

2. The four tanks are labeled as such:

```
| Tank 1 | Tank 2 |
| Tank 3 | Tank 4 |
```

3. Define a priority stack, with the first being highest priority.

```
tank_priority_stack: [4,1,3,2]
```


