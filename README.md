# The Gadget Snap

This gadget snap provides the boot assets required to boot the AllWinner Nezha.

Specifically, this gadget provides the u-boot binary and a GRUB binary which
search for the relevant partition expected of an Ubuntu Core system, depending
on if this is a fresh system with only a system-seed partition or an already
existing system with an ubuntu-boot partition.

## Usage

Because this gadget uses GRUB to boot the kernel, it should behave very
similarly to the reference gadget snaps maintained by Canonical. However,
successfully building this image requires using a forked version of [snapd](https://github.com/dilyn-corner/snapd/tree/grub-riscv) 
and [ubuntu-image](https://github.com/dilyn-corner/ubuntu-image/tree/grub-riscv), 
respectively. This is because some of the GRUB assets provided by snapd need to
be updated to support RISC-V systems, and ubuntu-image uses some snapd code to
generate these assets at image build time. A PR to add these changes to upstream
is forthcoming.

Also note that there are currently (as of March 29) no RISC-V64 core24 snaps
published in the store, and you will have to provide your own! You can find
a core24 base snap [here](https://github.com/snapcore/core-base), the `main`
branch should enable you to build a core24 base.

I would recommend building all of these snaps natively; the only one that is
easiest to cross-build is the gadget.

## Building

1) Build and install the ubuntu-image fork from above
2) Build the snapd snap fork from above
3) Build the core24 base snap from above
3) build this snap (and the corresponding [kernel snap](https://github.com/canonical/iot-field-kernel-snap/tree/devel-riscv64-nezha))
4) Create a model assertion (get inspiration from the [reference models](https://github.com/snapcore/models))
5) Build your image:

```
    ubuntu-image snap              \
        --snap path/to/base/snap   \
        --snap path/to/snapd/snap  \
        --snap path/to/gadget/snap \
        --snap path/to/kernel/snap \
        path/to/your/model
```

6) Write that image to an SD card (note that sdX is your SD card, this command
    is destructive to data):

```
    dd if=nezha.img of=/dev/sdX bs=1M status=progress conv=fsync
```

7) Insert the SD card and boot the board

Some current issues prevent fully automated installation; see the next section
for those issues and current workarounds.

## Current issues

- The boot process is not fully automated

Currently, one must enter the below in the u-boot console of the hardware via `screen`:

```
    load mmc 0:1 $kernel_addr_r /EFI/boot/grubriscv64.efi
    bootefi $kernel_addr_r
```

This is less than desirable; the earlier versions of this gadget used a
`boot.scr` file which fully automated the boot process. An investigation will
have to be done to determine what the u-boot binary in the archive expects to
source during the boot process.


- Currently, no output is visible when allowing GRUB config to manage the boot process

If one manually boots the kernel EFI binary at the GRUB prompt, kernel output
can be seen. However, if the builtin GRUB configuration loads the grub.cfg
from some partition, no output is seen. However, the boot process still occurs,
resulting in a successfully installed Ubuntu Core system. Upon rebooting, the
system won't be able to boot into the system in run mode.

Currently, one can do the below:

```
    loopback loop /systems/<system name>/snaps/nezha-kernel_<version>.snap
    chainloader (loop)/kernel.efi snapd_recovery_system=<system name> snapd_recovery_mode=install console=ttyS0 earlycon
```

The solution is somewhere in either the grub.builtin or in one of the snapd
managed bootloader assets.
