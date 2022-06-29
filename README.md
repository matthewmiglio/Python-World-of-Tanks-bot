# World-of-Tanks-bot

[![Python Versions](https://img.shields.io/pypi/pyversions/py-clash-bot)](https://www.python.org/downloads/) [![PyPI version](https://badge.fury.io/py/py-clash-bot.svg)](https://pypi.org/project/py-clash-bot/) [![GitHub Python Tests](https://github.com/matthewmiglio/py-clash-bot/actions/workflows/python-tests.yml/badge.svg)](https://github.com/matthewmiglio/py-clash-bot/actions/workflows/python-tests.yml) [![CodeFactor](https://www.codefactor.io/repository/github/matthewmiglio/py-clash-bot/badge)](https://www.codefactor.io/repository/github/matthewmiglio/Python-World-of-Tanks-bot)

A World of Tanks automation bot written in Python.

## Install

Choose one of the install methods below

#### a. Windows Install

[Download the latest release](https://github.com/matthewmiglio/Python-World-of-Tanks-bot).


### Configure client options

Graphics: 
    display mode: Windowed
    resolution: 1920x1020
    interface scaling: x1
    color adjustment: 1940s cine film

    *color adjustment is theoretically unnecessary but image recognition problems may occur on varying color adjustment settings.




## Run World-of-Tanks-bot

Before attempting to run the bot, make sure both the World of Tanks client is open.

#### a. Installed on Windows

Run the desktop shortcut the installer created.

## Configuration

Tank priority:
    -Available in configuration file
    -Select 4 tanks for the bot to use by checking each tank as primary.
    -Edit the configuration file to denote the priority of each tank (of the chosen 4)
    -format:
        -[priority1 tank, priority2 tank, priority3 tank, priority4 tank,]
        -[topleft, topright, bottomleft, bottomright]
        -ex: [4,1,3,2]
