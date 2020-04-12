# blugon

**A simple and configurable Blue Light Filter for X**

blugon is a simple and fast Blue Light Filter, that is highly configurable and provides a command line interface.
The program can be run just once or as a daemon (manually or via systemd).
There are several different backends available.
blugon calculates the screen color from your local time and configuration.

![blugon-comparison](https://github.com/jumper149/data/blob/master/blugon/comp.png?raw=true)
![blugon-simulation](https://github.com/jumper149/data/blob/master/blugon/sim.gif?raw=true)

### Comparison to other Blue Light Filters

blugon's main feature is the ability to control gamma values or color temperature at specific times of day.

|                          | blugon                    | [Redshift](https://github.com/jonls/redshift) | [f.lux](https://justgetflux.com/) |
|-------------------------:|:--------------------------|:----------------------------------------------|:----------------------------------|
| written in               | Python                    | C                                             | closed source                     |
| interface                | CLI                       | CLI or GUI                                    | GUI                               |
| timing configuration     | user defined              | day and night                                 | day and night                     |
| gamma configuration      | RGB values or temperature | temperature                                   | temperature                       |
| brightness configuration | none                      | none                                          | none                              |

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

### ArchLinux

There is an [AUR-Package](https://aur.archlinux.org/packages/blugon).

### Debian

    $ git clone https://github.com/jumper149/blugon.git
    $ sudo apt install gcc make python3 libx11-dev libxrandr-dev
    $ cd blugon/
    $ make PREFIX=/usr/local
    $ sudo make install PREFIX=/usr/local

### Nix

You can use the derivation from this [nix-expression](https://github.com/NixOS/nixpkgs/blob/55f4feb618f3178b7a384eaa914be2bef621af3e/pkgs/applications/misc/blugon/default.nix) in [nixpkgs](https://github.com/NixOS/nixpkgs).

### from source

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
