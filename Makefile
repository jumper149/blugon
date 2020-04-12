PREFIX := /usr

build:
	sed "s|MAKE_INSTALL_PREFIX = '.*'|MAKE_INSTALL_PREFIX = '$(PREFIX)'|g" blugon.py > blugon
	sed "s|MAKE_INSTALL_PREFIX|$(PREFIX)|g" systemd/user/blugon.service > blugon.service
	gcc -std=c99 -O2 -I /usr/X11R6/include -o backends/scg/scg backends/scg/scg.c -L /usr/X11R6/lib -lm -lX11 -lXrandr
	gzip --force --keep blugon.1

install:
	install -D -m755 blugon $(PREFIX)/bin/blugon
	install -D -m644 blugon.1.gz $(PREFIX)/share/man/man1/blugon.1.gz
	install -D -m644 bash-completion/blugon $(PREFIX)/share/bash-completion/completions/blugon
	install -D -m644 blugon.service $(PREFIX)/lib/systemd/user/blugon.service
	install -D -m755 backends/tty/tty.sh $(PREFIX)/lib/blugon/tty.sh
	install -D -m755 backends/scg/scg $(PREFIX)/lib/blugon/scg
	install -D -m644 configs/deepfried/gamma $(PREFIX)/share/blugon/configs/deepfried/gamma
	install -D -m644 configs/default/gamma $(PREFIX)/share/blugon/configs/default/gamma
	install -D -m644 configs/extreme/gamma $(PREFIX)/share/blugon/configs/extreme/gamma
	install -D -m644 configs/nothing/gamma $(PREFIX)/share/blugon/configs/nothing/gamma
	install -D -m644 configs/static/gamma $(PREFIX)/share/blugon/configs/static/gamma
	install -D -m644 configs/temperature/gamma $(PREFIX)/share/blugon/configs/temperature/gamma

clean:
	rm -f blugon
	rm -f backends/scg/scg
	rm -f blugon.1.gz
	rm -f blugon.service
