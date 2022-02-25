# The Gadget Snap

The gadget snap defines the structure & boot mechanisms of our device, amongst
many other things. As such, this snap is also quite device specific.

In this case, we are building u-boot to be carried as a payload for OpenSBI.
From there, we hope to exec the system, whether it be to bootstrap Ubuntu Core
or run as normal.

Much like the kernel, u-boot is very device specific. Modify
`snap/snapcraft.yaml` as necessary for your device.

Building:
`snapcraft --destructive-mode --target-arch=riscv64 --enable-experimental-target-arch`
