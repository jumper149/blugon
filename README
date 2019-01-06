# blugon
**A simple blue light filter written in Python**

The main purpose for it is to run in the background and change the gamma values of your screen depending on your local time.

## Usage
To use blugon as your daily blue light savior set up your configuration in `~/.config/blugon/`.

You can start blugon from the command line with `blugon`.

To fork it just use `blugon&` and stop it with `killall blugon`.

Other options include:

- `-c [dir]` or `--config [dir]` to specify configuration directory (default: `~/.config/blugon/`)
- `-s` or `--simulation` to quickly simulate the configuration for the whole day

## Install
For Archlinux users I am maintaining an AUR-Package: https://aur.archlinux.org/packages/blugon/

**Dependencies:**
- `python`
- `xorg-xgamma`
I am planning to support other backends later on, but for now you have to use xorg-xgamma.

If you are on Linux and want to install without package manager (please don't)  you can use:
- `make`
- `make install`

Configuration is supposed to be done after installing.

You can also use the script without installing it:
  `/usr/bin/pyhon blugon`

## Configuration
Examples for configurations can be found in `/usr/share/blugon/configs/`.

To use the default configuration you can use:
- `mkdir -p ~/.config/blugon/`
- `cp /usr/share/blugon/configs/default/gamma ~/.config/blugon/gamma`

For now the configuration only consists of the `gamma`-file.

