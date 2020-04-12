#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/extensions/Xrandr.h>

char *argv0 = "scg";

#define usage() fprintf(stderr, "usage: %s GAMMA_R GAMMA_G GAMMA_B\n", argv0)

#define die() do { usage(); exit(EXIT_FAILURE); } while (0)

double parse_arg(const char *arg)
{
    errno = 0;
    double gamma = strtod(arg, NULL);
    if (errno) {
        perror("strtod");
        die();
    }

    if (gamma < 0.0 || gamma > 1.0) {
        fprintf(stderr, "gamma values must be in 0.0 .. 1.0\n");
        die();
    }

    return gamma;
}

int main(int argc, char **argv)
{
    argv0 = argv[0];

    if (argc != 4) {
        die();
    }

    double gamma_r = parse_arg(argv[1]);
    double gamma_g = parse_arg(argv[2]);
    double gamma_b = parse_arg(argv[3]);

    Display *dpy = XOpenDisplay(NULL);
    if (dpy == NULL) {
        return 12; // exit code 12, if no display is found
    }

    Window root = XDefaultRootWindow(dpy);
    XRRScreenResources *res = XRRGetScreenResourcesCurrent(dpy, root);

    for (int c = 0; c < res->ncrtc; c++) {
        RRCrtc crtc = res->crtcs[c];
        int size = XRRGetCrtcGammaSize(dpy, crtc);
        XRRCrtcGamma *crtc_gamma = XRRAllocGamma(size);

        for (int i = 0; i < size; i++) {
            double g = 65535.0 * i / size;
            crtc_gamma->red[i]   = g * gamma_r;
            crtc_gamma->green[i] = g * gamma_g;
            crtc_gamma->blue[i]  = g * gamma_b;
        }

        XRRSetCrtcGamma(dpy, crtc, crtc_gamma);
        XRRFreeGamma(crtc_gamma);
    }

    XRRFreeScreenResources(res);
    XCloseDisplay(dpy);

    return EXIT_SUCCESS;
}

/*
 * This program is based on 'sct'.
 * https://flak.tedunangst.com/post/sct-set-color-temperature
 * https://flak.tedunangst.com/files/sct.c
 */
