# The Gadget Snap

This gadget snap provides the boot assets required to boot the AllWinner Nezha
and Sipeed LicheeRV.

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
can be tracked [here](https://github.com/snapcore/snapd/pull/14201).

One can optionally add [console-conf](https://github.com/snapcore/console-conf-snap) 
to the image, but having RISC-V versions of this snap available in the store is
[blocked](https://github.com/snapcore/console-conf-snap/pull/29) on snapd 2.64
being released for RISC-V to resolve an outstanding bug in snapd.


## Building

1) Build and install the ubuntu-image fork from above (`snapcraft`)
2) Build the snapd snap fork from above (`snapcraft --remote-build --build-for riscv64`)
3) build this snap (and the corresponding [kernel snap](https://github.com/canonical/iot-field-kernel-snap/tree/devel-riscv64-nezha))
4) Create a model assertion (get inspiration from the [reference models](https://github.com/snapcore/models))
5) Build your image:

```
    ubuntu-image snap              \
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

- No output is visible when allowing GRUB config to manage the boot process

For some reason unknown to the author, the `snapd_full_cmdline_args` value in
`systems/<date>/grubenv` is improperly generated; it uses the amd64 snippet
instead of the riscv64 snippet it *should* be using. A workaround exists:

```
    sudo partx -av nezha.img
    sudo mount /dev/loopXXp1 /mnt
    # Modify the snapd_full_cmdline_args line to read 'console=ttyS0,115200n8
    #   earlycon panic=-1' and delete five # marks
    sudo umount /mnt
    sudo partx -d /dev/loopXX
```

This will result in full boot output on the serial device output of the device.
