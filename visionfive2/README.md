# The Gadget Snap

This gadget snap provides the boot assets required to boot the StarFive
Visionfive2.

Specifically, this gadget provides the u-boot and SPL binaries, along with a
GRUB binary which search for the relevant partition expected of an Ubuntu Core
system, depending on if this is a fresh system with only a system-seed partition
or an already existing system with an ubuntu-boot partition.


## Usage

Because this gadget uses GRUB to boot the kernel, it should behave very
similarly to the reference gadget snaps maintained by Canonical. However,
successfully building this image requires using a forked version of [snapd](https://github.com/dilyn-corner/snapd/tree/grub-riscv) 
and [ubuntu-image](https://github.com/dilyn-corner/ubuntu-image/tree/grub-riscv), 
respectively. This is because some of the GRUB assets provided by snapd need to
be updated to support RISC-V systems, and ubuntu-image uses some snapd code to
generate these assets at image build time. A PR to add these changes to upstream
can be tracked [here](https://github.com/snapcore/snapd/pull/14201).


## Building

1) Build and install the ubuntu-image fork from above (`snapcraft`)
2) Build the snapd snap fork from above (`snapcraft --remote-build --build-for riscv64`)
3) build this snap (and the corresponding [kernel snap](https://github.com/canonical/iot-field-kernel-snap/tree/24-riscv64-visionfive2))
4) Create a model assertion (get inspiration from the [reference models](https://github.com/snapcore/models))
5) Build your image:

```sh
    ubuntu-image snap              \
        --snap path/to/snapd/snap  \
        --snap path/to/gadget/snap \
        --snap path/to/kernel/snap \
        path/to/your/model
```

6) One can optionally add [console-conf](https://github.com/snapcore/console-conf-snap) 
to the image, but having RISC-V versions of this snap available in the store is
[blocked](https://github.com/snapcore/console-conf-snap/pull/29) on snapd 2.64
being released for RISC-V to resolve an outstanding bug in snapd.

Alternatively, a system-user assertion can be added to the image:

```json
    {
        "type": "system-user",
        "authority-id": "<same ID which signed the model assertion>",
        "series": ["16"],
        "brand-id": "<same ID which signed the model assertion>",
        "email": "<your email address>",
        "models": ["<same as model name in model assertion"],
        "name": "<your name>",
        "username": "<your desired username>",
        "password": "<mkpasswd -m sha-512 -S <8CHARSALT> -s>",
        "since": "2023-01-16T18:06:04+00:00",
        "until": "2025-05-16T18:06:04+00:00"
    }
```


Sign with the same key which signed the model assertion:

```sh
    snap sign -k <model signing key> --chain auto-import.json > auto-import.assert
```

Put `auto-import.assert` in the `systems/<date>/` directory of the image you
create.


7) Write that image to an SD card (note that sdX is your SD card, this command
    is destructive to data):

```
    dd if=visionfive2.img of=/dev/sdX bs=1M status=progress conv=fsync
```

8) Insert the SD card and boot the board

Some current issues prevent fully automated installation; see the next section
for those issues and current workarounds.


## Current issues

- No output is visible when allowing GRUB config to manage the boot process

For some reason unknown to the author, the `snapd_full_cmdline_args` value in
`systems/<date>/grubenv` is improperly generated; it uses the amd64 snippet
instead of the riscv64 snippet it *should* be using. A workaround exists:

```sh
    sudo partx -av visionfive2.img
    sudo mount /dev/loopXXp1 /mnt
    # Modify the snapd_full_cmdline_args line to read 'console=ttyS0,115200n8
    #   earlycon panic=-1' and delete some # marks
    sudo umount /mnt
    sudo partx -d /dev/loopXX
```

This will result in full boot output on the serial device output of the device.

- One ethernet port works

Specifically, the *innermost* one. The Wiki claims only the outermost one works,
but that doesn't seem to be true :)

- USB does not work

This one is weird. No idea why :)

- GPU does not work

Again, weird. No idea why :)

- The DTB in-use isn't easy to specify

A DTB for both versions (1.2a, 1.3b) are available in `mmc 1:3 dtbs/starfive`.
GRUB might do the right thing, who knows! To specify:

```sh
    load mmc 1:3 $kernel_addr_r /EFI/boot/grubriscv64.efi
    load mmc 1:3 $fdt_addr_r    /dtbs/starfive/jh7110-starfive-visionfive-2-v1.2a.dtb
    bootefi $kernel_addr_r $fdt_addr_r
```

- The OS can't update any EFI entries

This is a u-boot limitation as far as I can tell; it really just means we should
be building u-boot ourselves :)

You can do the below, however. Note that my board booted with the correct DTB
after doing the following:

```sh
    efidebug boot add -b 0001 'Ubuntu Core 24' mmc 1:3 /EFI/boot/grubriscv64.efi
    efidebug boot order 0001
    bootefi bootmgr
```

The board should automagically boot from now on! Swap mmc for nvme if you are
using that, of course.
