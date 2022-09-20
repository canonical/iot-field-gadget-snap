# The Gadget Snap

The gadget snap defines the structure & boot mechanisms of our device, amongst
many other things. As such, this snap is also quite device specific.

In this case, we are building u-boot to be carried as a payload for OpenSBI.
From there, we hope to exec the system, whether it be to bootstrap Ubuntu Core
or run as normal.

Much like the kernel, u-boot is very device specific. Modify
`snap/snapcraft.yaml` as necessary for your device.

Building:

`snapcraft`


## Academic Information

There are several different ways of building OpenSBI, the Supervisor Binary
Interface for RISC-V (for more information, see [their project](https://github.com/riscv-software-src/opensbi)).

1) `fw_jump.elf`

    |-> Jumps to a specific location in memory and executes the object there

2) `fw_payload.elf`

    |-> Executes a binary built into OpenSBI as a pyaload

3) `fw_dynamic.elf`

    |-> Determines how to proceed to the next bootloader at run-time

`fw_dynamic.elf` is used in cases where `u-boot.bin` is built in m-mode
(`qemu-riscv64_spl_defconfig`). This is not our case here, so we will ignore it.

`fw_jump.elf` is useful in cases where we want to execute some arbitrary program
at a memory address; for all practical purposes, the thing we load is either
Linux or u-boot. So we don't need this.

`fw_payload.elf` is used when you know you want to execute the same payload
every time. This is specifically useful when the boot stage prior to OpenSBI
cannot execute *both* OpenSBI *and* the following boot stage. This is
interesting to us (at least in the Qemu case).


Therefore, we know that we must
1) build u-boot in smode (`qemu-riscv64_smode_defconfig`)
2) build OpenSBI with that `u-boot.bin` as `FW_PAYLOAD_PATH=/path/to/u-boot.bin`

Thus, this gadget has two primary binaries which are built:
1) u-boot.bin
2) fw_payload.elf

This is approximately all the knowledge required for us here.

There are some additional files to consider.

`boot.scr.in` file is processed at build-time to produce a set of
instructions which `u-boot.bin` will execute at run-time.

`gadget.yaml` defines the underlying structure of our Ubuntu Core image.

`fitImage.its` is an optional file in our use case but can be relevant when we
are using a u-boot built in M-mode (spl). This case will require a modified
`snap/snapcraft.yaml` in which we build u-boot twice, once as a payload for
OpenSBI and a second time as a binary containing that `fw_payload.elf`. This is
potentially relevant on *real hardware*.


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
issue, make an issue. If you have something to add, open a PR!
