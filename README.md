# blugon
**A simple blue light filter written in Python**

![blugon-simulation](https://thumbs.gfycat.com/LeanSnappyGemsbok.webp)

## Usage
To use blugon as your daily blue light savior set up your configuration in `~/.config/blugon/`.

You can start blugon from the command line with `blugon`.

To run it in the background just use `(blugon&)` and stop it with `killall blugon`.

Options include:

- `-s` or `--simulation` to quickly simulate the configuration for the whole day
- `-i [secs]` or `--interval=[secs]` to set time between refreshes
- `-c [dir]` or `--config=[dir]` to specify configuration directory
- `-b [backend]` or `--backend=[backend]` to choose the backend for communication with X11

## Configuration
Examples for configurations can be found in `/usr/share/blugon/configs/`.

To use the default configuration you can use:
- `mkdir -p ~/.config/blugon/`
- `cp /usr/share/blugon/configs/default/gamma ~/.config/blugon/gamma`

For now the configuration only consists of the `gamma`-file.

## Dependencies
- `python`
### optional:
- `xorg-xgamma` as backend
- `scg` as backend @ [GitHub](https://github.com/jumper149/scg), [AUR](https://aur.archlinux.org/packages/scg)

## Install
For Archlinux users I am maintaining an [AUR-Package](https://aur.archlinux.org/packages/blugon)

If you are on Linux you can build and install:
- `make`
- `make install`

Configuration is supposed to be done after installing.

You can also use the script without installing it:
  `/usr/bin/python3 blugon`
