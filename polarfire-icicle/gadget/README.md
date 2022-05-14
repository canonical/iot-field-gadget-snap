# The Gadget Snap

The gadget snap defines the structure & boot mechanisms of our device, amongst
many other things. As such, this snap is also quite device specific.

In this case, we are packaging an entire boot stack; from the zero stage
bootloader all the way up to our final bootloader (u-boot), which will land us
into a UC20 userspace.

Building:

`snapcraft --destructive-mode --target-arch=riscv64 --enable-experimental-target-arch`


## Academic Information

The Sipeed Lichee RV has some specific requirements to boot!

This board's bootrom is setup to execute the zero stage bootloader at a specific
point on disk, and we likewise require a cfg file to be at a specific location
on disk.

This cfg file will detail the location OpenSBI, the device tree, and the u-boot
binary are to be loaded into memory. more importantly, this cfg file also
*contains* the relevant binary and dtb files. As such, this gadget builds many
components, but only ships a few objects; the relevant early-stage boot files
are bundled in a single file and written to a nonpartition on the device image.

**NOTE**: this board has an optional dock! This particular branch builds with
the dock in mind -- if you are using the board without its optional dock, be
sure to modify the relevant device tree names!

**NOTE**: while the dock includes an HDMI port, the only way to get output to it
requires modifying `sysfs`:

```
echo disp0                      > /sys/kernel/debug/dispdbg/name
echo switch1                    > /sys/kernel/debug/dispdbg/command
echo 4 10 0 0 0x4 0x101 0 0 0 8 > /sys/kernel/debug/dispdbg/param
echo 1                          > /sys/kernel/debug/dispdbg/start
```

This could potentially be added to a snap to allow this output by default on
Ubuntu Core. However, I do not believe any currently existing interfaces allow
modifying this particular `sysfs` location. You could use a devmode snap in the
meantime.

Currently, this gadget snap is in some way broken. Without a UART connection, I
cannot debug; this should be solved soon(tm).

For some very useful resources on this board specifically,

[Building a bootable rootfs](https://andreas.welcomes-you.com/boot-sw-debian-risc-v-lichee-rv/)

[Useful board facts](https://linux-sunxi.org/Sipeed_Lichee_RV)

[Fedora's writeup](https://fedoraproject.org/wiki/Architectures/RISC-V/Allwinner)


## For Beginners

If you are new to hardware enablement and board bring-up, welcome!

Here are some good resources I found for RISC-V:

[RISC-V bootflow, explained](https://crvf2019.github.io/pdf/43.pdf)

[RISC-V bootflow (with examples!)](https://riscv.org/wp-content/uploads/2019/12/Summit_bootflow.pdf)

[OpenSBI explainer](https://github.com/riscv-software-src/opensbi)

[OpenSBI firmware explainer](https://github.com/riscv-software-src/opensbi/tree/master/docs/firmware)

[Embedded Linux from Scratch](https://youtube.com/watch?v=cIkTh3Xp3dA)

Some important things to know:

1) There is high variation between boards. You will more than likely have to
    tweak a few things to get your particular board working.

2) Some boards simply aren't supported, whether by u-boot or the kernel
    itself. The best way is to add support yourself. The easiest way is to
    get someone else to do it for you.

3) Given that you have to modify some files, what may they be? 
    * It's unlikely that you'll have to modify the `gadget.yaml` too much
    
    * You'll have to use a different config than the one provided by
      `u-boot/config`. Building u-boot is similar to building the kernel;
      get the sources, do `make foo_defconfig` for your hardware, 
      `make menuconfig` to tweak.
    
    * You'll have to tweak the addresses defined in `u-boot/boot.scr.in` -
      these are very much specific to your board, as the amount of RAM
      varies per device and what address `u-boot` reserves for itself can be
      different. Useful tools in `u-boot` include `md`, `bdi`.

Example: Qemu's virt board reserves all memory address prior to 0x80000000 (2G).
Given a 2G machine, all available address are 0x80000000 to 0xffffffff. However,
some of this memory is occupied; Qemu injects its device tree into OpenSBI on
your behalf, and so a small portion of addressable space is already occupied by
that. Just poke an address to see what's available. Your board's manual might
also include some helpful information.

4) Slight modifications will be needed for `snap/snapcraft.yaml`,
    particularly to modify the `make foo_defconfig` invocation.

Ultimately, it's a game of tweak-rebuild-reflash. Eventually, you'll get to the
kernel. And from there, it's a whole new ball game.


If you have any questions, don't hesitate to ask (email)! If you identify an
issue, make an Issue. If you have something to add, open a PR!
