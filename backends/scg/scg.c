#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>
#include <X11/extensions/Xrandr.h>

double parse_arg(const char *arg) {
    errno = 0;
    double gamma = strtod(arg, NULL);
    if (errno) {
        perror("strtod");
        exit(EXIT_FAILURE);
    }

    return gamma;
}

int parse_int_arg(const char *arg) {
    errno = 0;
    int num = strtol(arg, NULL, 10);
    if (errno) {
        perror("strtol");
        exit(EXIT_FAILURE);
    }

    return num;
}

int main(int argc, char **argv) {
    char *output = NULL;
    if (argc < 4 || argc > 5) {
        exit(EXIT_FAILURE);
    }
    if (argc >= 5) {
        output = argv[4];
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

    RRCrtc output_crtc = 0;
    if (output != NULL) {
        for (int m = 0; m < res->noutput; m++) {
            XRROutputInfo *oi = XRRGetOutputInfo(dpy, res, res->outputs[m]);
            if (!strcmp(oi->name, output))
                output_crtc = oi->crtc;
            XRRFreeOutputInfo(oi);
        }
        if (!output_crtc) {
            fprintf(stderr, "could not find crtc for output %s\n", output);
            exit(EXIT_FAILURE);
        }
    }

    for (int c = 0; c < res->ncrtc; c++) {
        RRCrtc crtc = res->crtcs[c];
        if (output_crtc && crtc != output_crtc)
            continue;
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
