The Polarfire Icicle Kit boots the HSS on the eNVM. That HSS then executes some
payload binary and the system runs from there, with the HSS initially booted
running in the background.

As a result, we don't actually need to build our own HSS in the gadget. We
simply need to create the payload file for HSS to execute. In this case, that
would be u-boot.

A different HSS can be flashed to the board using the Libero software suite
provided by Microchip. A free license can be obtained for at least
non-commercial uses.

I don't know how to use their tooling to create the proper files to flash a
custom-built HSS to this hardware. If you happen to know, feel free to drop me a
line. I have simply gone ahead and used the one available from their [releases](https://github.com/polarfire-soc/icicle-kit-reference-design/releases)

Building:

`snapcraft`


## Academic Information

The Icicle Developer Kit is based off Microchip's Polarfire SoC. The board
itself has a ton of really interesting features, and - more interestingly for
this project - has a somewhat unique way of moving from a first stage bootloader
to the operating system!

Let's explore how the Icicle kit boots.

Per [The "official" docs](https://u-boot.readthedocs.io/en/latest/board/microchip/mpfs_icicle.html#risc-v-polarfire-soc):

> The current U-Boot port is supported in S-mode only and loaded from DRAM.
> A prior stage M-mode firmware/bootloader (e.g. HSS with OpenSBI) is required
> to boot the u-boot.bin in S-mode.

The current setup for our bootloader is that the HSS firmware is built with the
`u-boot-dtb.bin` as a payload, leveraging the bundled OpenSBI binary HSS builds.

With this in mind, we will use Microchip's boot-flow:

`HSS + OpenSBI (M-Mode) -> U-Boot (S-Mode) -> Linux (S-Mode)`

What this essentially means is that we will build u-boot, and from there, we
will use the `hss-payload-generator` to parse a [YAML file](hss/hss.yaml)
which defines what payload(s) are delivered by the HSS firmware during boot, and
where they are loaded from.

There is an important thing to note about this bootflow!

HSS is launched from the eNVM on the board during boot. HSS has gotten very
large since 2020. So big, in fact, that special care has to be taken when
building it. Unfortunately, this special care is not present on sufficiently
recent Ubuntu systems (I haven't tested any systems earlier than 20.04, YMMV).


 > As a result of this, we truly only support and test against the compiler
 > bundled with Microchip SoftConsole. While other toolchains can work,
 > they may indeed have certain issues at any particular point in time.

[Sauce](https://github.com/polarfire-soc/hart-software-services/issues/19)

 > If you are building using the SoftConsole toolchain (which is our
 > supported toolchain for the HSS) you should not see this issue.

[Sauce](https://github.com/polarfire-soc/hart-software-services/issues/30)

As a result, we should build with the SoftConsole toolchain. I think it is bad
praxis to bundle toolchains, so I will not be bundling this (not to mention the
EULA one must accept in order to use it -- I have no intention of gathering
legal flak for this). However, you can download it from [here](https://www.microchip.com/en-us/products/fpgas-and-plds/fpga-and-soc-design-tools/soc-fpga/softconsole#downloads).


You can find more information on this hardware, how to boot and update it, and
more from the following sources:
[Official documentation](https://github.com/polarfire-soc/polarfire-soc-documentation)

[Developing on this hardware](https://github.com/polarfire-soc/polarfire-soc-documentation/blob/master/boards/mpfs-icicle-kit-es/icicle-kit-sw-developer-guide/icicle-kit-sw-developer-guide.md)

[Updating the hardware](https://github.com/polarfire-soc/polarfire-soc-documentation/blob/master/boards/mpfs-icicle-kit-es/updating-icicle-kit/updating-icicle-kit-design-and-linux.md)


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
    * You'll likely have to make minimal changes to `gadget.yaml`

    * You'll have to use a different config for u-boot. Building u-boot is
      similar to building the kernel; get the sources, do `make foo_defconfig`
      for your hardware, `make menuconfig` to tweak.

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
issue, make an issue. If you have something to add, open a PR!
