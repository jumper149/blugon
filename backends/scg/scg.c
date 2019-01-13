#include <X11/Xlib.h>
#include <X11/Xproto.h>
#include <X11/Xatom.h>
#include <X11/extensions/Xrandr.h>

#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv) {
	Display *dpy = XOpenDisplay(NULL);
	int screen = DefaultScreen(dpy);
	Window root = RootWindow(dpy, screen);

	XRRScreenResources *res = XRRGetScreenResourcesCurrent(dpy, root);

	double gamma_r;
	double gamma_g;
	double gamma_b;

	/* parsing */
	if (argc == 4) {
		gamma_r = atof(argv[1]);
		gamma_g = atof(argv[2]);
		gamma_b = atof(argv[3]);
	}else {
		return 1;
	}

	int num_crtcs = res->ncrtc;
	for (int c = 0; c < res->ncrtc; c++) {
		int crtcxid = res->crtcs[c];
		XRRCrtcInfo *crtc_info = XRRGetCrtcInfo(dpy, res, crtcxid);

		int size = XRRGetCrtcGammaSize(dpy, crtcxid);

		XRRCrtcGamma *crtc_gamma = XRRAllocGamma(size);

		for (int i = 0; i < size; i++) {
			double g = 65535.0 * i / size;
			crtc_gamma->red[i]   = g * gamma_r;
			crtc_gamma->green[i] = g * gamma_g;
			crtc_gamma->blue[i]  = g * gamma_b;
		}
		XRRSetCrtcGamma(dpy, crtcxid, crtc_gamma);

		XFree(crtc_gamma);
	}
	return 0;
}

/*
 * This program is based on 'sct'
 * Source: https://https.www.google.com.tedunangst.com/flak/post/sct-set-color-temperature
 *         https://https.www.google.com.tedunangst.com/flak/files/sct.c
 */
