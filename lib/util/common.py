#! /home/chenli/Documents/tools/anaconda3/envs/pytorch/bin/python
# coding: utf-8

import os
import pickle
import logging
import multiprocessing


### 全局锁
# pylint: disable=invalid-name
global_lock = multiprocessing.Lock()


def prepare_dir(path):
    """Make dir if necessary."""

    dirname = os.path.dirname(path)
    ### 当前目录直接返回
    if not dirname: return None

    if not os.path.exists(dirname):
        with global_lock:
            os.makedirs(dirname)
    return None


def dump_to_file(data, path):
    """dump data to file."""

    prepare_dir(path)
    with open(path, "wb") as dstfile:
        pickle.dump(data, dstfile, protocol=2)


def initialize_logger(name=None, file=None, display=True):
    """Configurate logger based on settings.

    Args:
        name: str. Logger name, 'None' means root logger.
        file: str. Path of file to log to, 'None' or empty string to disable
            logging to file.
        display: bool. Indicate whether the logger logs to console or not.

    Returns:
        The required logger instance.
    """

    logger = logging.getLogger(name)
    if logger.handlers: return logger

    ### 局部的logger是全局logger的child, 这里防止局部的log扩散到全局log中
    logger.propagate = False
    logger.setLevel(logging.INFO)

    fmt = "%(asctime)s %(filename)s:%(lineno)d] %(levelname)s: %(message)s"
    fmt = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    if file:
        prepare_dir(file)
        handler = logging.FileHandler(file)
        handler.setFormatter(fmt)
        logger.addHandler(handler)

    if display:
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)

    return logger


def COLOR(text, color):
    ansi_colors = {
        "black":     "0;30",    "bright black":     "0;90",
        "red":       "0;31",    "bright red":       "0;91",
        "green":     "0;32",    "bright green":     "0;92",
        "yellow":    "0;33",    "bright yellow":    "0;93",
        "blue":      "0;34",    "bright blue":      "0;94",
        "magenta":   "0;35",    "birght magenta":   "0;95",
        "cyan":      "0;36",    "bright cyan":      "0;96",
        "white":     "0;37",    "brignt white":     "0;97",
    }
    all_colors = {}
    for key, value in ansi_colors.items():
        all_colors[key.lower().replace(" ", "")] = value
    all_colors["gray"] = ansi_colors["bright black"]

    color = color.lower().replace(" ", "")
    assert color in all_colors, f"Unknown color: {color}"
    return f"\033[{all_colors[color]}m{text}\033[0m"


def BLACK(text):    return COLOR(text, "black")    # noqa: E704
def RED(text):      return COLOR(text, "red")      # noqa: E704
def GREEN(text):    return COLOR(text, "green")    # noqa: E704
def YELLOW(text):   return COLOR(text, "yellow")   # noqa: E704
def BLUE(text):     return COLOR(text, "blue")     # noqa: E704
def MAGENTA(text):  return COLOR(text, "magenta")  # noqa: E704
def CYAN(text):     return COLOR(text, "cyan")     # noqa: E704
def WHITE(text):    return COLOR(text, "white")    # noqa: E704
def GRAY(text):     return COLOR(text, "gray")     # noqa: E704


if __name__ == "__main__":
    pass
