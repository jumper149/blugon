PREFIX := /usr

build:
	sed "s|MAKE_INSTALL_PREFIX = '.*'|MAKE_INSTALL_PREFIX = '$(PREFIX)'|g" blugon.py > blugon
	gcc -std=c99 -O2 -I /usr/X11R6/include -o backends/scg/scg backends/scg/scg.c -L /usr/X11R6/lib -lm -lX11 -lXrandr
	gzip --force --keep blugon.1

install:
	install -d $(PREFIX)/bin/
	install -m755 blugon $(PREFIX)/bin/blugon
	install -d $(PREFIX)/share/man/man1/
	install -m644 blugon.1.gz $(PREFIX)/share/man/man1/
	install -d $(PREFIX)/share/bash-completion/completions/
	install -m644 bash-completion/blugon $(PREFIX)/share/bash-completion/completions/blugon
	install -d $(PREFIX)/lib/systemd/user/
	install -m644 systemd/user/blugon.service $(PREFIX)/lib/systemd/user/
	install -d $(PREFIX)/lib/blugon/
	install -m755 backends/tty/tty.sh $(PREFIX)/lib/blugon/
	install -m755 backends/scg/scg $(PREFIX)/lib/blugon/
	install -d $(PREFIX)/share/blugon/configs/deepfried/
	install -m644 configs/deepfried/gamma $(PREFIX)/share/blugon/configs/deepfried/
	install -d $(PREFIX)/share/blugon/configs/default/
	install -m644 configs/default/gamma $(PREFIX)/share/blugon/configs/default/
	install -d $(PREFIX)/share/blugon/configs/extreme/
	install -m644 configs/extreme/gamma $(PREFIX)/share/blugon/configs/extreme/
	install -d $(PREFIX)/share/blugon/configs/nothing/
	install -m644 configs/nothing/gamma $(PREFIX)/share/blugon/configs/nothing/
	install -d $(PREFIX)/share/blugon/configs/static/
	install -m644 configs/static/gamma $(PREFIX)/share/blugon/configs/static/
	install -d $(PREFIX)/share/blugon/configs/temperature/
	install -m644 configs/temperature/gamma $(PREFIX)/share/blugon/configs/temperature/

clean:
	rm -f blugon
	rm -f backends/scg/scg
	rm -f blugon.1.gz
