#!/usr/bin/python3

from configparser import ConfigParser
from argparse import ArgumentParser
import time
import math
from subprocess import check_call
from os import getenv
from sys import stdout

MAKE_INSTALL_PREFIX = '/usr'

#--------------------------------------------------DEFAULTS

VERSION = '1.6'

DISPLAY = getenv('DISPLAY')

ONCE = False

SIMULATE = False

INTERVAL = 120

CONFIG_DIR = getenv('XDG_CONFIG_HOME')
if not CONFIG_DIR:
    CONFIG_DIR = getenv('HOME') + '/.config'
CONFIG_DIR += '/blugon'

BACKEND = 'scg'

#--------------------------------------------------DEFINITIONS

MAX_MINUTE = 24 * 60

KELVIN_MIN = 1000
KELVIN_MAX = 12000
KELVIN_STEP = 100
KELVIN_RGB_TABLE = {
    1000:  (255,  56,   0),
    1100:  (255,  71,   0),
    1200:  (255,  83,   0),
    1300:  (255,  93,   0),
    1400:  (255, 101,   0),
    1500:  (255, 109,   0),
    1600:  (255, 115,   0),
    1700:  (255, 121,   0),
    1800:  (255, 126,   0),
    1900:  (255, 131,   0),
    2000:  (255, 138,  18),
    2100:  (255, 142,  33),
    2200:  (255, 147,  44),
    2300:  (255, 152,  54),
    2400:  (255, 157,  63),
    2500:  (255, 161,  72),
    2600:  (255, 165,  79),
    2700:  (255, 169,  87),
    2800:  (255, 173,  94),
    2900:  (255, 177, 101),
    3000:  (255, 180, 107),
    3100:  (255, 184, 114),
    3200:  (255, 187, 120),
    3300:  (255, 190, 126),
    3400:  (255, 193, 132),
    3500:  (255, 196, 137),
    3600:  (255, 199, 143),
    3700:  (255, 201, 148),
    3800:  (255, 204, 153),
    3900:  (255, 206, 159),
    4000:  (255, 209, 163),
    4100:  (255, 211, 168),
    4200:  (255, 213, 173),
    4300:  (255, 215, 177),
    4400:  (255, 217, 182),
    4500:  (255, 219, 186),
    4600:  (255, 221, 190),
    4700:  (255, 223, 194),
    4800:  (255, 225, 198),
    4900:  (255, 227, 202),
    5000:  (255, 228, 206),
    5100:  (255, 230, 210),
    5200:  (255, 232, 213),
    5300:  (255, 233, 217),
    5400:  (255, 235, 220),
    5500:  (255, 236, 224),
    5600:  (255, 238, 227),
    5700:  (255, 239, 230),
    5800:  (255, 240, 233),
    5900:  (255, 242, 236),
    6000:  (255, 243, 239),
    6100:  (255, 244, 242),
    6200:  (255, 245, 245),
    6300:  (255, 246, 247),
    6400:  (255, 248, 251),
    6500:  (255, 249, 253),
    6600:  (254, 249, 255),
    6700:  (252, 247, 255),
    6800:  (249, 246, 255),
    6900:  (247, 245, 255),
    7000:  (245, 243, 255),
    7100:  (243, 242, 255),
    7200:  (240, 241, 255),
    7300:  (239, 240, 255),
    7400:  (237, 239, 255),
    7500:  (235, 238, 255),
    7600:  (233, 237, 255),
    7700:  (231, 236, 255),
    7800:  (230, 235, 255),
    7900:  (228, 234, 255),
    8000:  (227, 233, 255),
    8100:  (225, 232, 255),
    8200:  (224, 231, 255),
    8300:  (222, 230, 255),
    8400:  (221, 230, 255),
    8500:  (220, 229, 255),
    8600:  (218, 229, 255),
    8700:  (217, 227, 255),
    8800:  (216, 227, 255),
    8900:  (215, 226, 255),
    9000:  (214, 225, 255),
    9100:  (212, 225, 255),
    9200:  (211, 224, 255),
    9300:  (210, 223, 255),
    9400:  (209, 223, 255),
    9500:  (208, 222, 255),
    9600:  (207, 221, 255),
    9700:  (207, 221, 255),
    9800:  (206, 220, 255),
    9900:  (205, 220, 255),
    10000: (207, 218, 255),
    10100: (207, 218, 255),
    10200: (206, 217, 255),
    10300: (205, 217, 255),
    10400: (204, 216, 255),
    10500: (204, 216, 255),
    10600: (203, 215, 255),
    10700: (202, 215, 255),
    10800: (202, 214, 255),
    10900: (201, 214, 255),
    11000: (200, 213, 255),
    11100: (200, 213, 255),
    11200: (199, 212, 255),
    11300: (198, 212, 255),
    11400: (198, 212, 255),
    11500: (197, 211, 255),
    11600: (197, 211, 255),
    11700: (197, 210, 255),
    11800: (196, 210, 255),
    11900: (195, 210, 255),
    12000: (195, 209, 255)}

COLOR_TABLE = {
        0:  '282a2e',
        1:  'a54242',
        2:  '8c9440',
        3:  'de935f',
        4:  '5f819d',
        5:  '85678f',
        6:  '5e8d87',
        7:  '707880',
        8:  '373b41',
        9:  'cc6666',
        10: 'b5bd68',
        11: 'f0c674',
        12: '81a2be',
        13: 'b294bb',
        14: '8abeb7',
        15: 'c5c8c6'}

BACKEND_LIST = [ 'xgamma', 'scg', 'tty' ]

#--------------------------------------------------PARSER

argparser = ArgumentParser(prog='blugon', description="A simple Blue Light Filter for X")

argparser.add_argument('-v', '--version', action='store_true', dest='version', help='print version and exit')
argparser.add_argument('-p', '--printconfig', action='store_true', dest='printconfig', help='print default configuration and exit')
argparser.add_argument('-o', '--once', action='store_true', dest='once', help='apply configuration for current time and exit')
argparser.add_argument('-s', '--simulation', action='store_true', dest='simulate', help='simulate blugon over one day and exit')
argparser.add_argument('-i', '--interval', nargs='?', dest='interval', type=float, help='set %(dest)s in seconds (default: '+str(INTERVAL)+')')
argparser.add_argument('-c', '--config', nargs='?', dest='config_dir', type=str, help='set configuration directory (default: '+CONFIG_DIR+')')
argparser.add_argument('-b', '--backend', nargs='?', dest='backend', type=str, help='set backend (default: '+BACKEND+')')

args = argparser.parse_args()

if args.version:
    print('blugon ' + VERSION)
    exit()

#--------------------------------------------------CONFIG

                                               #---ARGUMENTS
if args.config_dir:
    CONFIG_DIR = args.config_dir
if not CONFIG_DIR.endswith('/'):
    CONFIG_DIR += '/'
CONFIG_FILE_GAMMA = CONFIG_DIR + 'gamma'
CONFIG_FILE_GAMMA_FALLBACK = MAKE_INSTALL_PREFIX + '/share/blugon/configs/default/gamma'
CONFIG_FILE_CONFIG = CONFIG_DIR + 'config'
                                               #---ARGUMENTS END

confparser = ConfigParser()
confparser['main'] = {
        'interval': str(INTERVAL),
        'backend':  BACKEND      }

confparser['tty'] = {
        'color0':  str(COLOR_TABLE[0]) ,
        'color1':  str(COLOR_TABLE[1]) ,
        'color2':  str(COLOR_TABLE[2]) ,
        'color3':  str(COLOR_TABLE[3]) ,
        'color4':  str(COLOR_TABLE[4]) ,
        'color5':  str(COLOR_TABLE[5]) ,
        'color6':  str(COLOR_TABLE[6]) ,
        'color7':  str(COLOR_TABLE[7]) ,
        'color8':  str(COLOR_TABLE[8]) ,
        'color9':  str(COLOR_TABLE[9]) ,
        'color10': str(COLOR_TABLE[10]),
        'color11': str(COLOR_TABLE[11]),
        'color12': str(COLOR_TABLE[12]),
        'color13': str(COLOR_TABLE[13]),
        'color14': str(COLOR_TABLE[14]),
        'color15': str(COLOR_TABLE[15])}

if args.printconfig:
    confparser.write(stdout)
    exit()

confparser.read(CONFIG_FILE_CONFIG)

confs = confparser['main']

#--------------------------------------------------ARGUMENTS

ONCE = args.once

SIMULATE = args.simulate

INTERVAL = confs.getint('interval')
if args.interval:
    INTERVAL = math.ceil(args.interval)

BACKEND = confs.get('backend')
if args.backend:
    BACKEND = args.backend
if not BACKEND in BACKEND_LIST:
    raise ValueError('backend not found, choose from:\n    ' + '\n    '.join(BACKEND_LIST))

if (not DISPLAY) and (BACKEND != 'tty'):
    exit(11) # provide exit status 11 for systemd-service

#--------------------------------------------------FUNCTIONS

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

    try:
        file_gamma = open(CONFIG_FILE_GAMMA, 'r')
    except:
        #print('Using fallback gamma configuration file: \'' + CONFIG_FILE_GAMMA_FALLBACK + '\'')
        file_gamma = open(CONFIG_FILE_GAMMA_FALLBACK, 'r')
    unfiltered_gamma = list(map(line_to_list, file_gamma.read().splitlines()))
    file_gamma.close()

    gamma = list(filter(lambda x : x, unfiltered_gamma))
    list(filter(check_len, gamma))
    gamma = list(map(time_to_minutes, gamma))
    gamma.sort(key=take_first)
    minutes = (list(map(pop_first, gamma)))
    return gamma, minutes

def temp_to_gamma(temp):
    """transforms temperature in kelvin to gamma values"""
    if temp < KELVIN_MIN or temp > KELVIN_MAX:
        raise ValueError('temperature values have to be between ' + str(KELVIN_MIN) + ' and ' + str(KELVIN_MAX))
    temp_lower = KELVIN_STEP * int(math.floor(temp / KELVIN_STEP))
    temp_upper = temp_lower + KELVIN_STEP
    factor = (temp - temp_lower) / KELVIN_STEP
    red_lower, green_lower, blue_lower = KELVIN_RGB_TABLE[temp_lower]
    red_upper, green_upper, blue_upper = KELVIN_RGB_TABLE[temp_upper]
    red_gamma = (factor * red_lower + (1 - factor) * red_upper) / 255
    green_gamma = (factor * green_lower + (1 - factor) * green_upper) / 255
    blue_gamma = (factor * blue_lower + (1 - factor) * blue_upper) / 255
    return red_gamma, green_gamma, blue_gamma

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

def call_xgamma(red_gamma, green_gamma, blue_gamma):
    """start subprocess of backend xorg-xgamma"""
    str_red_gamma = str(red_gamma)
    str_green_gamma = str(green_gamma)
    str_blue_gamma = str(blue_gamma)
    check_call(['xgamma', '-quiet', '-rgamma', str_red_gamma, '-ggamma', str_green_gamma, '-bgamma', str_blue_gamma])
    return

def call_scg(red_gamma, green_gamma, blue_gamma):
    """start subprocess of backend scg"""
    str_red_gamma = str(red_gamma)
    str_green_gamma = str(green_gamma)
    str_blue_gamma = str(blue_gamma)
    check_call([MAKE_INSTALL_PREFIX + '/lib/blugon/scg', str_red_gamma, str_green_gamma, str_blue_gamma])
    return

def call_tty(red_gamma, green_gamma, blue_gamma):
    """start subprocess of backend tty"""
    def hex_tempered(i):
        color = COLOR_TABLE[i]
        def flt_to_hex(flt):
            if flt > 255:
                flt = 255
            return format(int(flt), 'x')
        hex_r = flt_to_hex(red_gamma * int(color[0:2], 16))
        hex_g = flt_to_hex(green_gamma * int(color[2:4], 16))
        hex_b = flt_to_hex(blue_gamma * int(color[4:6], 16))
        string = format(i, 'X') + hex_r + hex_g + hex_b
        return string
    hex_list = [ hex_tempered(i) for i in range(16) ]
    check_call([MAKE_INSTALL_PREFIX + '/lib/blugon/tty.sh'] + hex_list)
    return

def call_backend(backend, red_gamma, green_gamma, blue_gamma):
    """wrapper to call various backends"""
    if backend == 'xgamma':
        call_xgamma(red_gamma, green_gamma, blue_gamma)
    elif backend == 'scg':
        call_scg(red_gamma, green_gamma, blue_gamma)
    elif backend == 'tty':
        call_tty(red_gamma, green_gamma, blue_gamma)
    return

def get_minute():
    """returns the current minute"""
    time_struct = time.localtime()
    minute = 60 * time_struct.tm_hour + time_struct.tm_min + time_struct.tm_sec / 60
    return minute

def reprint_time(minute):
    """prints time in a human readable format"""
    str_hour = ('00' + str(int(minute // 60)))[-2:]
    str_minute = ('00' + str(int(minute % 60)))[-2:]
    print('\r' + str_hour + ':' + str_minute, end='')
    return

#--------------------------------------------------MAIN

def main():
    LIST_GAMMA, LIST_MINUTES = read_gamma()

    def while_body(minute, sleep_time=0):
        """puts everything together to have only one function to call"""
        red_gamma, green_gamma, blue_gamma = calc_gamma(minute, LIST_MINUTES, LIST_GAMMA)
        call_backend(BACKEND, red_gamma, green_gamma, blue_gamma)
        try:
            time.sleep(sleep_time)
        except:
            exit()
        return

    if ONCE:
        while_body(get_minute(), 0)
        exit()

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
