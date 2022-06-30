import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from os.path import dirname, join
from typing import Union

import cv2
import numpy
import pyautogui
from joblib import Parallel, delayed
from PIL import Image


def screenshot(region=(0, 0, 1920, 1080)):
    if region is None:
        return pyautogui.screenshot()
    else:
        return pyautogui.screenshot(region=region)


def coords_is_equal(coords_A,coords_B,tol=30):
    if (coords_A is None)or(coords_B is None):
        return
    coords_1_diff=abs(coords_A[0]-coords_B[0])
    coords_2_diff=abs(coords_A[1]-coords_B[1])
    if (coords_1_diff<tol)and(coords_2_diff<tol):
        return True
    return False
    

def get_avg_pix(region):
    left = region[0]
    top = region[1]
    width = region[2]
    height = region[3]

    pixels = numpy.array(screenshot((left, top, width, height)))
    d1, d2, d3 = pixels.shape
    pixels = pixels.reshape((d1*d2, d3))
    avg_pix = numpy.mean(pixels, axis=0)
    return avg_pix
              
            
def print_avg_pixels(avg_pixels):
    column_count = 19
    current_column = 1
    for avg_pix in avg_pixels:
        avg_pix = ["%03d" % (num, ) for num in avg_pix]
        print(avg_pix, end="" if current_column % column_count != 0 else "\n")
        current_column = current_column+1


def get_first_location(locations: list[Union[list[int], None]], flip=False):
    """get the first location from a list of locations

    Args:
        locations (list[list[int]]): list of locations
        flip (bool, optional): flip coordinates. Defaults to False.

    Returns:
        list[int]: location
    """
    for location in locations:
        if location is not None:
            return [location[1], location[0]] if flip else location
    return None


def check_for_location(locations: list[Union[list[int], None]]):
    """check for a location

    Args:
        locations (list[list[int]]): _description_

    Returns:
        bool: if location is found or not
    """
    for location in locations:
        if location is not None:
            return True
    return False


def find_references(screenshot: Union[numpy.ndarray,
                                      Image.Image],
                    folder: str,
                    names: list[str],
                    tolerance=0.97) -> list[Union[list[int], None]]:
    """find reference images in a screenshot

    Args:
        screenshot (Union[np.ndarray, Image.Image]): find references in screenshot
        folder (str): folder to find references (from within reference_images)
        names (list[str]): names of references
        tolerance (float, optional): tolerance. Defaults to 0.97.

    Returns:
        list[Union[list[int], None]: coordinate locations
    """
    num_cores = multiprocessing.cpu_count()
    with ThreadPoolExecutor(num_cores) as ex:
        futures = [ex.submit(find_reference, screenshot,
                             folder, name, tolerance) for name in names]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                return [result]
    return [None]


def find_all_references(screenshot: Union[numpy.ndarray,
                                          Image.Image],
                        folder: str,
                        names: list[str],
                        tolerance=0.97) -> list[Union[list[int], None]]:
    """find all reference images in a screenshot

    Args:
        screenshot (Union[np.ndarray, Image.Image]): find references in screenshot
        folder (str): folder to find references (from within reference_images)
        names (list[str]): names of references
        tolerance (float, optional): tolerance. Defaults to 0.97.

    Returns:
        list[Union[list[int],None]]: coordinate locations
    """
    num_cores = multiprocessing.cpu_count()

    return Parallel(
        n_jobs=num_cores,
        prefer="threads")(
        delayed(find_reference)(
            screenshot,
            folder,
            name,
            tolerance) for name in names)


def find_reference(screenshot: Union[numpy.ndarray,
                                     Image.Image],
                   folder: str,
                   name: str,
                   tolerance=0.97):
    """find a reference image in a screenshot
    
    Args:
        screenshot (Union[np.ndarray, Image.Image]): find reference in screenshot
        folder (str): folder to find reference (from within reference_images)
        name (str): name of reference
        tolerance (float, optional): tolerance. Defaults to 0.97.

    Returns:
        Union[list[int], None]: coordinate location
    """
    top_level = dirname(__file__)
    reference_folder = join(top_level, "reference_images")
    return compare_images(
        screenshot,
            Image.open(
            join(
                reference_folder,
                folder,
                name)),
        tolerance)


def pixel_is_equal(pix1, pix2, tol):
    """check pixel equality

    Args:
        pix1 (list[int]): [R,G,B] pixel
        pix2 (list[int]): [R,G,B] pixel
        tol (float): tolerance

    Returns:
        bool: are pixels equal
    """
    diff_r = abs(pix1[0] - pix2[0])
    diff_g = abs(pix1[1] - pix2[1])
    diff_b = abs(pix1[2] - pix2[2])
    return (diff_r < tol) and (diff_g < tol) and (diff_b < tol)


def compare_images(image: Union[numpy.ndarray,
                                Image.Image],
                   template: Union[numpy.ndarray,
                                   Image.Image],
                   threshold=0.8):
    """detects pixel location of a template in an image
    Args:
        image (Union[np.ndarray, Image.Image]): image to find template within
        template (Union[np.ndarray, Image.Image]): template image to match to
        threshold (float, optional): matching threshold. defaults to 0.8
    Returns:
        Union[list[int], None]: a list of pixel location (x,y)
    """

    # show template
    # template.show()

    # Convert image to np.array

    image = numpy.array(image)
    template = numpy.array(template)

    # Convert image colors
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Store the coordinates of matched area in a numpy array
    loc = numpy.where(res >= threshold)  # type: ignore

    if len(loc[0]) != 1:
        return None

    return [int(loc[0][0]), int(loc[1][0])]
