# blugon
**A simple Blue Light Filter for X**

blugon is a simple and fast Blue Light Filter, that is highly configurable and provides a command line interface.
The program can be run just once or as a daemon (manually or via systemd).
There are several different backends available.

![blugon-comparison](https://github.com/jumper149/data/blob/master/blugon/comp.png?raw=true)
![blugon-simulation](https://github.com/jumper149/data/blob/master/blugon/sim.gif?raw=true)

## Usage
You can start blugon from the command line with `blugon`.

To run it in the background just use `(blugon&)` and stop it with `killall blugon`.

To run blugon with systemd you can enable the service as user:

    systemctl --user enable blugon.service

Append the following piece of code to your `~/.bashrc` to run blugon when you log into your TTY:

    if [ "$TERM" = "linux" ]; then
      blugon --once --backend="tty" && clear
      (blugon --backend="tty")&
    fi

### Options:
- `-o` or `--once` to apply gamma values of the current time
- `-s` or `--simulation` to quickly simulate the configuration for the whole day
- `-i [secs]` or `--interval=[secs]` to set time between refreshes
- `-c [path]` or `--configdir=[path]` to specify configuration directory
- `-b [backend]` or `--backend=[backend]` to choose the backend for communication with X11

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
