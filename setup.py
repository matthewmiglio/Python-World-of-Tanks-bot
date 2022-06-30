import os
from glob import glob

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# get github workflow env vars
try:
    version = (os.environ['GIT_TAG_NAME']).replace('v', '')
except KeyError:
    print('Defaulting to 0.0.0')
    version = '0.0.0'

# get files to include in dist
dist_files = [file.replace('wotbot/', '')
              for file in glob("wotbot/reference_images/*/*.png")]

setup(
    name='wotbot',
    version=version,
    description='World of Tanks Bot',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='world of tanks ai bot',
    author='Matthew Miglio',
    url='https://matthewmiglio.github.io/python-world-of-tanks-bot/',
    download_url='https://matthewmiglio.github.io/python-world-of-tanks-bot/releases/',
    install_requires=[
        'pillow',
        'opencv-python',
        'numpy',
        'pydirectinput',
        'pygetwindow',
        'matplotlib',
        'pyautogui',
        'joblib',
        'keyboard'],
    packages=['wotbot'],
    include_package_data=True,
    package_data={
        'wotbot': dist_files},
    python_requires='>=3.10',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
