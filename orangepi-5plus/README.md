# ODROID-HC4 Gadget Snap

Gadget snap for running Ubuntu Core 20 on the [ODROID-HC4](https://www.hardkernel.com/shop/odroid-hc4/).

Kernel snap: https://github.com/IsaacJT/odroid-hc4-kernel-snap

Important: the SPI flash must be erased on the board to force it to boot from the SD card.

# Building

Please note that due to a bug in the U-Boot code (https://github.com/hardkernel/u-boot/issues/73) the package `libfdt-dev` cannot be installed at the same time. This can cause issues when building the kernel snap on the same system as that needs this package.
