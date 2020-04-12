DESTDIR :=
PREFIX := /usr

build:
	sed "s|MAKE_INSTALL_PREFIX = '.*'|MAKE_INSTALL_PREFIX = '$(PREFIX)'|g" blugon.py > blugon
	sed "s|MAKE_INSTALL_PREFIX|$(PREFIX)|g" systemd/user/blugon.service > blugon.service
	gcc -std=c99 -O2 -I /usr/X11R6/include -o backends/scg/scg backends/scg/scg.c -L /usr/X11R6/lib -lm -lX11 -lXrandr
	gzip --best --force --keep blugon.1

install:
	install -D -m755 blugon $(DESTDIR)$(PREFIX)/bin/blugon
	install -D -m644 blugon.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/blugon.1.gz
	install -D -m644 bash-completion/blugon $(DESTDIR)$(PREFIX)/share/bash-completion/completions/blugon
	install -D -m644 blugon.service $(DESTDIR)$(PREFIX)/lib/systemd/user/blugon.service
	install -D -m755 backends/tty/tty.sh $(DESTDIR)$(PREFIX)/lib/blugon/tty.sh
	install -D -m755 backends/scg/scg $(DESTDIR)$(PREFIX)/lib/blugon/scg
	install -D -m644 configs/deepfried/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/deepfried/gamma
	install -D -m644 configs/default/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/default/gamma
	install -D -m644 configs/extreme/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/gamma
	install -D -m644 configs/nothing/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/nothing/gamma
	install -D -m644 configs/static/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/static/gamma
	install -D -m644 configs/temperature/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/temperature/gamma

clean:
	rm -f blugon
	rm -f backends/scg/scg
	rm -f blugon.1.gz
	rm -f blugon.service
