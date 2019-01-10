PREFIX := /usr

build:
	gcc -std=c99 -O2 -I /usr/X11R6/include -o backends/scg/scg backends/scg/scg.c -L /usr/X11R6/lib -lm -lX11 -lXrandr
	gzip --force --keep blugon.1

install:
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m755 blugon.py $(DESTDIR)$(PREFIX)/bin/blugon
	install -d $(DESTDIR)$(PREFIX)/share/man/man1/
	install -m644 blugon.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/
	install -d $(DESTDIR)$(PREFIX)/lib/systemd/user/
	install -m644 systemd/user/blugon.service $(DESTDIR)$(PREFIX)/lib/systemd/user/
	install -d $(DESTDIR)$(PREFIX)/lib/blugon/
	install -m755 backends/tty/tty.sh $(DESTDIR)$(PREFIX)/lib/blugon/
	install -m755 backends/scg/scg $(DESTDIR)$(PREFIX)/lib/blugon/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -m644 configs/default/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
	install -m644 configs/extreme/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/nothing/
	install -m644 configs/nothing/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/nothing/
