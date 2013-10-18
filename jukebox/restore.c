// Restores the framebuffer console after a failed framebuffer display

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <linux/input.h>
#include <linux/kd.h>
#include <sys/ioctl.h>

int main (int argc, char *argv[])
{
    int tty;
    tty = open("/dev/tty1", O_RDWR);
    ioctl(tty, KDSETMODE, KD_TEXT);
}
