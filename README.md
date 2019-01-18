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
- `(blugon&)` to start
- `killall blugon` to stop

To run blugon with systemd you can enable the service as user:

    systemctl --user enable blugon.service

You can use the current-mode to manually control color temperature (with keybinds for example; doesn't need daemon):
- `blugon --setcurrent="+600"` for more blue
- `blugon --setcurrent="-600"` for more red

Append the following piece of code to your `~/.bashrc` to run blugon when you log into your TTY:

    if [ "$TERM" = "linux" ]; then
      blugon --once --backend="tty" && clear
      (blugon --backend="tty")&
    fi

For further help you can use the `-h` flag or the more intensive man-page:

    man blugon

### Options:
- `-o` or `--once` to apply gamma values of the current time
- `-S` or `--setcurrent` to set or change the current color temperature
- `-s` or `--simulation` to quickly simulate the configuration for the whole day
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
- `make`
- `make install`

To change the target directory of the installation use something similar to:

    make install PREFIX=/usr/local

Configuration is supposed to be done after installing.
