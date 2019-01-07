#!/usr/bin/python3

from argparse import ArgumentParser
import time
import math
from subprocess import check_call
from os import getenv

VERSION = '1.1'

INTERVAL = 120

CONFIG_DIR = getenv('XDG_CONFIG_HOME')
if not CONFIG_DIR:
    CONFIG_DIR = getenv('HOME') + '/.config'
CONFIG_DIR += '/blugon'

SIMULATE = False

#-----------------------------------------------------------------

parser = ArgumentParser(prog='blugon', description="A blue light filter written in 'Python' using 'xgamma' as backend")

parser.add_argument('-v', '--version', action='store_true', dest='version', help='print version and exit')
parser.add_argument('-i', '--interval', nargs='?', dest='interval', type=float, const=INTERVAL, default=INTERVAL, help='set %(dest)s in seconds (default: '+str(INTERVAL)+')')
parser.add_argument('-c', '--config', nargs='?', dest='config_dir', type=str, const=CONFIG_DIR, default=CONFIG_DIR, help='set configuration directory (default: '+CONFIG_DIR+')')
parser.add_argument('-s', '--simulation', action='store_true', dest='simulate', help="simulate 'blugon' over one day and exit")

#-----------------------------------------------------------------

args = parser.parse_args()

if args.version:
    print("blugon " + VERSION)
    exit()

INTERVAL = math.ceil(args.interval)

CONFIG_DIR = args.config_dir
if not CONFIG_DIR.endswith('/'):
    CONFIG_DIR += '/'
CONFIG_FILE_GAMMA = CONFIG_DIR + "gamma"

SIMULATE = args.simulate

#-----------------------------------------------------------------

MAX_MINUTE = 24 * 60

#-----------------------------------------------------------------

def read_gamma():
    """
    reads configuration of gamma values from CONFIG_FILE_GAMMA
    returns 2 lists: gamma, minutes
    """
    def line_to_list(line):
        str_list = line.split()
        if not str_list: # remove empty line
            return False
        if str_list[0].startswith('#'): # remove comment
            return False
        float_list = list(map(float, str_list)) # gamma values
        return float_list
    def check_len(ls):
        if not (len(ls)==5):
            raise ValueError('gamma configuration requires syntax:\n    [hour] [minute]   [red-gamma] [green-gamma] [blue-gamma]')
    def time_to_minutes(ls):
        ls[0] = int(60 * ls[0] + ls[1])
        del ls[1]
        return ls
    def take_first(ls):
        return ls[0]
    def pop_first(ls):
        x = ls[0]
        del ls[0]
        return x
    with open(CONFIG_FILE_GAMMA, 'r') as file_gamma:
        unfiltered_gamma = list(map(line_to_list, file_gamma.read().splitlines()))
    gamma = list(filter(lambda x : x, unfiltered_gamma))
    list(filter(check_len, gamma))
    gamma = list(map(time_to_minutes, gamma))
    gamma.sort(key=take_first)
    minutes = (list(map(pop_first, gamma)))
    return gamma, minutes

def get_minute():
    """returns the current minute"""
    time_struct = time.localtime()
    minute = 60 * time_struct.tm_hour + time_struct.tm_min + time_struct.tm_sec / 60
    return minute

def call_xgamma(red_gamma, green_gamma, blue_gamma):
    """change screen color with backend xorg-xgamma"""
    str_red_gamma = str(red_gamma)
    str_green_gamma = str(green_gamma)
    str_blue_gamma = str(blue_gamma)
    check_call(['xgamma', '-quiet', '-rgamma', str_red_gamma, '-ggamma', str_green_gamma, '-bgamma', str_blue_gamma])
    return

def calc_gamma(minute, list_minutes, list_gamma):
    """calculates the RGB gamma values"""
    next_index = list_minutes.index(next((x for x in list_minutes if x >= minute), list_minutes[0]))
    next_minute = list_minutes[next_index]
    prev_minute = list_minutes[next_index - 1]
    if next_minute < prev_minute:
        next_minute += MAX_MINUTE

    def inbetween_gamma(next_gamma, prev_gamma):
        """calculates gamma value with linear regression"""
        diff_gamma = next_gamma - prev_gamma
        diff_minute = next_minute - prev_minute
        add_minute = minute - prev_minute
        try:
            factor = add_minute / diff_minute
        except:
            factor = 0
        gamma = prev_gamma + factor * diff_gamma
        return gamma

    next_red = list_gamma[next_index][0]
    prev_red = list_gamma[next_index - 1][0]
    next_green = list_gamma[next_index][1]
    prev_green = list_gamma[next_index - 1][1]
    next_blue = list_gamma[next_index][2]
    prev_blue = list_gamma[next_index - 1][2]

    red_gamma = inbetween_gamma(next_red, prev_red)
    green_gamma = inbetween_gamma(next_green, prev_green)
    blue_gamma = inbetween_gamma(next_blue, prev_blue)

    return red_gamma, green_gamma, blue_gamma

def reprint_time(minute):
    """prints time in a human readable format"""
    str_hour = ('00' + str(int(minute // 60)))[-2:]
    str_minute = ('00' + str(int(minute % 60)))[-2:]
    print('\r' + str_hour + ':' + str_minute, end='')
    return

#-----------------------------------------------------------------

def main():
    LIST_GAMMA, LIST_MINUTES = read_gamma()

    def while_body(minute, sleep_time=0):
        """puts everything together to have only one function to call"""
        red_gamma, green_gamma, blue_gamma = calc_gamma(minute, LIST_MINUTES, LIST_GAMMA)
        call_xgamma(red_gamma, green_gamma, blue_gamma)
        try:
            time.sleep(sleep_time)
        except:
            exit()
        return

    if SIMULATE:
        current_minute = get_minute()
        steps = 100
        sleep_time = 1 / 50
        for step in range(0, steps):
            minute = (current_minute + step * MAX_MINUTE / steps) % MAX_MINUTE
            reprint_time(minute)
            while_body(minute, sleep_time)
        print() # print newline
        while_body(current_minute)
        exit()

    while True :
        while_body(get_minute(), INTERVAL)

    return

if __name__ == "__main__":
    main()
