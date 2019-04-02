# blugon
**A simple Blue Light Filter for X**

blugon is a simple and fast Blue Light Filter, that is highly configurable and provides a command line interface.
The program can be run just once or as a daemon (manually or via systemd).
There are several different backends available.
blugon calculates the screen color from your local time and configuration.

![blugon-comparison](https://github.com/jumper149/data/blob/master/blugon/comp.png?raw=true)
![blugon-simulation](https://github.com/jumper149/data/blob/master/blugon/sim.gif?raw=true)

## Usage
You can start blugon from the command line:

    blugon

To run it in the background just use:

    (blugon&)         # to start
    killall blugon    # to stop

To run blugon with systemd you can enable the service as user:

    systemctl --user enable blugon.service

You can use the current-mode to manually control color temperature (with keybinds for example; doesn't need daemon):

    blugon --setcurrent="+600"    # for more blue
    blugon --setcurrent="-600"    # for more red

For further help you can use the `-h` flag or the more intensive man-page:

    man blugon

### Options:
- `-o` or `--once` to apply gamma values of the current time
- `-S` or `--setcurrent` to set or change the current color temperature
- `-s` or `--simulation` to quickly simulate the configuration for the whole day
- `-f` or `--fade` to fade in screen color on startup
- `-i [secs]` or `--interval=[secs]` to set time between refreshes
- `-c [path]` or `--configdir=[path]` to specify configuration directory
- `-b [backend]` or `--backend=[backend]` to choose the backend for communication with X

### available backends:
- `xgamma` - most compatible, requires optional dependency
- `scg` - best result
- `tty` - to run blugon on your TTY

## Configuration
Examples for configurations can be found in `/usr/share/blugon/configs/`.

To use the default configuration as a template you can use:

    mkdir -p ~/.config/blugon/
    cp /usr/share/blugon/configs/default/gamma ~/.config/blugon/gamma
    blugon --printconfig > ~/.config/blugon/config

## Dependencies
- `python`
- `libx11`
- `libxrandr`
### optional:
- `xorg-xgamma` as backend

## Install
For ArchLinux users I am maintaining an [AUR-Package](https://aur.archlinux.org/packages/blugon).

If you are on Linux you can build and install:

    make
    make install    # as root

To change the target directory of the installation use the following and change `/usr/local` to the desired directory:

    make PREFIX=/usr/local
    make install PREFIX=/usr/local

Configuration is supposed to be done after installing.

## Contributing
Feel free to Fork, create Issues and make Pull Requests.

I am looking forward to finding Package Maintainers and will happily accept improvements in the source code.
