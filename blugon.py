#!/usr/bin/python3

from configparser import ConfigParser
from argparse import ArgumentParser
import time
import math
from subprocess import check_call
from os import getenv
from sys import stdout

MAKE_INSTALL_PREFIX = '/usr'

#----------------------------------------------------------------------DEFAULTS

VERSION = '1.11.1'

VERBOSE = False

DISPLAY = getenv('DISPLAY')

WAIT_FOR_X = False
SLEEP_AFTER_FAILED_STARTUP = 0.1
SLEEP_AFTER_LOSING_X = 120.0

ONCE = False

READCURRENT = False

CURRENT_TEMP = None
CURRENT_TEMP_ADD = False

SIMULATE = False

FADE = False
FADE_STEPS = 10
FADE_DURATION = 3.0

INTERVAL = 120

CONFIG_DIR = getenv('XDG_CONFIG_HOME')
if not CONFIG_DIR:
    CONFIG_DIR = getenv('HOME') + '/.config'
CONFIG_DIR += '/blugon'

BACKEND = 'scg'

#----------------------------------------------------------------------DEFINITIONS

MAX_MINUTE = 24 * 60

NORMAL_TEMP = 6600.0

MIN_CURRENT_TEMP = 1.0
MAX_CURRENT_TEMP = 20000.0

NORMAL_RED = 1.0
NORMAL_GREEN = 1.0
NORMAL_BLUE = 1.0

BACKEND_LIST = [ 'xgamma', 'scg', 'tty' ]

COLOR_TABLE = {       # VGA colors from https://en.wikipedia.org/wiki/ANSI_escape_code
        0:  '000000',
        1:  'aa0000',
        2:  '00aa00',
        3:  'aa5500',
        4:  '0000aa',
        5:  'aa00aa',
        6:  '00aaaa',
        7:  'aaaaaa',
        8:  '555555',
        9:  'ff5555',
        10: '55ff55',
        11: 'ffff55',
        12: '5555ff',
        13: 'ff55ff',
        14: '55ffff',
        15: 'ffffff'}

#----------------------------------------------------------------------PARSER

argparser = ArgumentParser(prog='blugon', description='A simple Blue Light Filter for X')

argparser.add_argument('-v', '--version', action='store_true',
        dest='version', help='print version and exit')
argparser.add_argument('-V', '--verbose', action='store_true',
        dest='verbose', help='display additional information to debug')
argparser.add_argument('-p', '--printconfig', action='store_true',
        dest='printconfig', help='print default configuration and exit')
argparser.add_argument('-o', '--once', action='store_true',
        dest='once', help='apply configuration for current time and exit')
argparser.add_argument('-r', '--readcurrent', action='store_true',
        dest='readcurrent', help='read temperature from '+CONFIG_DIR+'/current')
argparser.add_argument('-S', '--setcurrent', nargs='?',
        dest='current_temp', type=str, help='set current temperature configuration, implies -r')
argparser.add_argument('-s', '--simulation', action='store_true',
        dest='simulate', help='simulate blugon over one day and exit')
argparser.add_argument('-f', '--fade', action='store_true',
        dest='fade', help='slowly fade color on startup')
argparser.add_argument('-i', '--interval', nargs='?',
        dest='interval', type=float, help='set %(dest)s in seconds (default: '+str(INTERVAL)+')')
argparser.add_argument('-c', '--configdir', '--config', nargs='?',
        dest='config_dir', type=str, help='set configuration directory (default: '+CONFIG_DIR+')')
argparser.add_argument('-b', '--backend', nargs='?',
        dest='backend', type=str, help='set backend (default: '+BACKEND+')')
argparser.add_argument('-w', '--waitforx', action='store_true',
        dest='wait_for_x', help='continue when backend fails')

args = argparser.parse_args()

if args.version:
    print('blugon ' + VERSION)
    exit()

VERBOSE = args.verbose

#----------------------------------------------------------------------CONFIG

                                                                   #---ARGUMENTS
if args.config_dir:
    CONFIG_DIR = args.config_dir
if not CONFIG_DIR.endswith('/'):
    CONFIG_DIR += '/'
CONFIG_FILE_GAMMA = CONFIG_DIR + 'gamma'
CONFIG_FILE_GAMMA_FALLBACK = MAKE_INSTALL_PREFIX + '/share/blugon/configs/default/gamma'
CONFIG_FILE_CONFIG = CONFIG_DIR + 'config'
CONFIG_FILE_CURRENT = CONFIG_DIR + 'current'
                                                                   #---ARGUMENTS END

confparser = ConfigParser()
confparser['main'] = {
        'readcurrent': str(READCURRENT),
        'interval':    str(INTERVAL)   ,
        'backend':     BACKEND         ,
        'wait_for_x':  str(WAIT_FOR_X) ,
        'fade':        str(FADE)       }

confparser['current'] = {
        'min_temp': str(MIN_CURRENT_TEMP),
        'max_temp': str(MAX_CURRENT_TEMP)}

confparser['wait_for_x'] = {
        'sleep_after_failed_startup': str(SLEEP_AFTER_FAILED_STARTUP),
        'sleep_after_losing_x':       str(SLEEP_AFTER_LOSING_X)      }

confparser['fade'] = {
        'steps':    str(FADE_STEPS)   ,
        'duration': str(FADE_DURATION)}

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

#----------------------------------------------------------------------ARGUMENTS

ONCE = args.once

MIN_CURRENT_TEMP = confparser['current'].getfloat('min_temp')
MAX_CURRENT_TEMP = confparser['current'].getfloat('max_temp')

READCURRENT = confs.getboolean('readcurrent')
if args.readcurrent:
    READCURRENT = args.readcurrent

if args.current_temp:
    if args.current_temp[0] in ['+', '-']:
        CURRENT_TEMP_ADD = True
    CURRENT_TEMP = float(args.current_temp)
    ONCE = True
    READCURRENT = True

INTERVAL = confs.getint('interval')
if args.interval:
    INTERVAL = math.ceil(args.interval)

BACKEND = confs.get('backend')
if args.backend:
    BACKEND = args.backend
if not BACKEND in BACKEND_LIST:
    raise ValueError('backend not found, choose from:\n    ' + '\n    '.join(BACKEND_LIST))

WAIT_FOR_X = confs.getboolean('wait_for_x')
if args.wait_for_x:
    WAIT_FOR_X = args.wait_for_x
SLEEP_AFTER_FAILED_STARTUP = confparser['wait_for_x'].getfloat('sleep_after_failed_startup')
SLEEP_AFTER_LOSING_X = confparser['wait_for_x'].getfloat('sleep_after_losing_x')

SIMULATE = args.simulate

FADE = confs.getboolean('fade')
if args.fade:
    FADE = args.fade
FADE_STEPS = confparser['fade'].getint('steps')
FADE_DURATION = confparser['fade'].getfloat('duration')

for i in range(15):
    COLOR_TABLE[i] = confparser['tty'].get('color' + str(i))

#----------------------------------------------------------------------FUNCTIONS

def verbose_print(string):
    if VERBOSE and (not SIMULATE):
        print(string)
    return

def temp_to_gamma(temp):
    """
    Transforms temperature in Kelvin to Gamma values between 0 and 1.
    Source: http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    def rgb_to_gamma(color):
        if color < 0:
            color = 0
        if color > 255:
            color = 255
        return color / 255

    temp = temp / 100

    if temp <= 66:                               # red
        r = 255
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)

    if temp <= 66:                               # green
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)

    if temp <= 10:                               # blue
        b = 0
    elif temp >= 66:
        b = 255
    else:
        b = temp - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307

    return map(rgb_to_gamma, (r, g, b))

def read_gamma():
    """
    Reads configuration of Gamma values from 'CONFIG_FILE_GAMMA'
    Returns 2 lists: gamma, minutes
    """
    def line_to_list(line):
        str_ls = line.split()
        if not str_ls:                    # remove empty line
            return False
        if str_ls[0].startswith('#'):     # remove comment
            return False
        flt_ls = list(map(float, str_ls)) # to gamma values
        return flt_ls
    def check_length(ls):
        length = len(ls)
        if (not (length==5 or length==3)):
            raise ValueError('gamma configuration requires syntax:\n'
                    '    [hour] [minute]   [red-gamma] [green-gamma] [blue-gamma]\n'
                    'or  [hour] [minute]   [temperature]')
        if length==3:                      # handle temperature configuration
            r, g, b = temp_to_gamma(ls[2])
            del ls[2]
            ls = ls + [r, g, b]
        return ls
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
        verbose_print('Using gamma configuration file: \'' +
                CONFIG_FILE_GAMMA + '\'')
        file_gamma = open(CONFIG_FILE_GAMMA, 'r')
    except:
        verbose_print('Using fallback gamma configuration file: \'' +
                CONFIG_FILE_GAMMA_FALLBACK + '\'')
        file_gamma = open(CONFIG_FILE_GAMMA_FALLBACK, 'r')
    gamma = list(map(line_to_list, file_gamma.read().splitlines()))
    file_gamma.close()

    gamma = list(filter(lambda x : x, gamma)) # removes empty lines and comments
    gamma = list(map(check_length, gamma))    # sanity check, temperature to gamma
    gamma = list(map(time_to_minutes, gamma))
    gamma.sort(key=take_first)                # sort by time
    minutes = (list(map(pop_first, gamma)))
    return gamma, minutes

def read_current(return_temp=False):
    """
    Reads temperature from 'CONFIG_FILE_CURRENT'
    Returns 3 Gamma values as floats: red, green, blue
    With argument return_temp=True return temperature value
    """
    try:
        verbose_print('Using current configuration file: \'' +
                CONFIG_FILE_CURRENT + '\'')
        file_current = open(CONFIG_FILE_CURRENT, 'r')
    except:
        raise ValueError('current configuration file not found at:\n'
                '    ' + CONFIG_FILE_CURRENT + '\n\n' +
                'To create this file use:\n' + '    blugon --setcurrent=' + str(NORMAL_TEMP))

    try:
        temp = float(file_current.readline())
    except:
        raise ValueError('current configuration file requires syntax:\n'
                '    [temp]\n'
                'temperature value as float, nothing else, no whitespace etc.')
    file_current.close()

    if return_temp:
        return temp

    r, g, b = temp_to_gamma(temp)
    verbose_print('Calculated RGB Gamma values: ' + str(r) + ' ' +  str(g) + ' ' + str(b))
    return r, g, b

def set_current():
    """Sets 'CURRENT_TEMP' to 'CONFIG_FILE_CURRENT'"""
    if CURRENT_TEMP_ADD:
        try:
            temp = read_current(return_temp=True) + CURRENT_TEMP
        except:
            temp = NORMAL_TEMP + CURRENT_TEMP
    else:
        temp = CURRENT_TEMP

    if temp < MIN_CURRENT_TEMP:
        verbose_print('Temperature wanted to be set capped at minimum ' + str(MIN_CURRENT_TEMP))
        temp = MIN_CURRENT_TEMP
    elif temp > MAX_CURRENT_TEMP:
        verbose_print('Temperature wanted to be set capped at maximum ' + str(MAX_CURRENT_TEMP))
        temp = MAX_CURRENT_TEMP

    verbose_print('Writing temperature ' + str(temp) +
                ' to current configuration file: \'' + CONFIG_FILE_CURRENT + '\'')
    with open(CONFIG_FILE_CURRENT, 'w') as file_current:
        file_current.write(str(temp))
    return

def calc_gamma(minute, list_minutes, list_gamma):
    """Calculates the RGB Gamma values inbetween configured times"""
    next_index = list_minutes.index(next((x for x in list_minutes if x >= minute), list_minutes[0]))
    next_minute = list_minutes[next_index]
    prev_minute = list_minutes[next_index - 1]
    if next_minute < prev_minute:
        next_minute += MAX_MINUTE

    def inbetween_gamma(next_gamma, prev_gamma):
        """Calculates Gamma value with a linear function"""
        diff_gamma = next_gamma - prev_gamma
        diff_minute = (next_minute - prev_minute) % MAX_MINUTE
        add_minute = (minute - prev_minute) % MAX_MINUTE
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

    verbose_print('Calculated RGB Gamma values: ' +
            str(red_gamma) + ' ' +  str(green_gamma) + ' ' + str(blue_gamma))
    return red_gamma, green_gamma, blue_gamma

def call_xgamma(red_gamma, green_gamma, blue_gamma):
    """Start a subprocess of backend xorg-xgamma"""
    str_red_gamma = str(red_gamma)
    str_green_gamma = str(green_gamma)
    str_blue_gamma = str(blue_gamma)
    check_call(['xgamma', '-quiet', '-rgamma', str_red_gamma,
        '-ggamma', str_green_gamma, '-bgamma', str_blue_gamma])
    return

def call_scg(red_gamma, green_gamma, blue_gamma):
    """Start a subprocess of backend scg"""
    str_red_gamma = str(red_gamma)
    str_green_gamma = str(green_gamma)
    str_blue_gamma = str(blue_gamma)
    check_call([MAKE_INSTALL_PREFIX + '/lib/blugon/scg',
        str_red_gamma, str_green_gamma, str_blue_gamma])
    return

def call_tty(red_gamma, green_gamma, blue_gamma):
    """Start a subprocess of backend tty"""
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
    """Wrapper to call various backends"""
    verbose_print('Calling backend ' + backend)
    if backend == 'xgamma':
        call_xgamma(red_gamma, green_gamma, blue_gamma)
    elif backend == 'scg':
        call_scg(red_gamma, green_gamma, blue_gamma)
    elif backend == 'tty':
        call_tty(red_gamma, green_gamma, blue_gamma)
    return

def get_minute():
    """Returns the current minute"""
    time_struct = time.localtime()
    minute = 60 * time_struct.tm_hour + time_struct.tm_min + time_struct.tm_sec / 60
    verbose_print('Provide current minute ' + str(minute))
    return minute

def reprint_time(minute):
    """Prints time in a human readable format"""
    str_hour = ('00' + str(int(minute // 60)))[-2:]
    str_minute = ('00' + str(int(minute % 60)))[-2:]
    print('\r' + str_hour + ':' + str_minute, end='')
    return

def gamma_step(red_gamma, green_gamma, blue_gamma, max_step, step):
    """Returns appropriate gamma values for step considering fading"""
    red = red_gamma + (NORMAL_RED - red_gamma) * ((max_step - step) / max_step)
    green = green_gamma + (NORMAL_GREEN - green_gamma) * ((max_step - step) / max_step)
    blue = blue_gamma + (NORMAL_BLUE - blue_gamma) * ((max_step - step) / max_step)
    return red, green, blue

#----------------------------------------------------------------------SANITY

if (not DISPLAY) and (BACKEND != 'tty'):
    verbose_print('DISPLAY environment variable not set')
    if WAIT_FOR_X:
        time.sleep(SLEEP_AFTER_FAILED_STARTUP)
    exit(11)

#----------------------------------------------------------------------MAIN

def main():
    if CURRENT_TEMP:
        set_current()

    if READCURRENT:
        CURRENT = read_current()
    else:
        LIST_GAMMA, LIST_MINUTES = read_gamma()

    def while_body(minute, sleep_time=0):
        """Puts everything together to have only one function to call"""
        if READCURRENT:
            red_gamma, green_gamma, blue_gamma = CURRENT
        else:
            red_gamma, green_gamma, blue_gamma = calc_gamma(minute, LIST_MINUTES, LIST_GAMMA)
        if WAIT_FOR_X: # allows switching to another TTY
            try:
                call_backend(BACKEND, red_gamma, green_gamma, blue_gamma)
            except:
                verbose_print('Waiting for X-server')
                time.sleep(SLEEP_AFTER_LOSING_X)
        else:
            call_backend(BACKEND, red_gamma, green_gamma, blue_gamma)
        try:
            verbose_print('Wait for ' + str(sleep_time) + ' seconds')
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

    if FADE and (BACKEND != 'tty'):
        current_minute = get_minute()
        steps = FADE_STEPS
        sleep_time = FADE_DURATION / steps
        verbose_print('Fading in ' + str(steps) + ' steps over ' + str(FADE_DURATION)  + ' seconds')
        if READCURRENT:
            main_red_gamma, main_green_gamma, main_blue_gamma = CURRENT
        else:
            main_red_gamma, main_green_gamma, main_blue_gamma = calc_gamma(current_minute, LIST_MINUTES, LIST_GAMMA)
        for step in range(0, steps):
            red_gamma, green_gamma, blue_gamma = gamma_step(main_red_gamma, main_green_gamma, main_blue_gamma, steps, step)
            if WAIT_FOR_X:
                try:
                    call_backend(BACKEND, red_gamma, green_gamma, blue_gamma)
                except:
                    verbose_print('X-server not found, cancel fading')
                    return
            else:
                call_backend(BACKEND, red_gamma, green_gamma, blue_gamma)
            time.sleep(sleep_time)

    if ONCE:
        while_body(get_minute(), 0)
        exit()


    while True :
        while_body(get_minute(), INTERVAL)

    return

if __name__ == "__main__":
    main()
