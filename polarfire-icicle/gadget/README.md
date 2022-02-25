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


## Academic Information

The gadget has two primary binaries which are built:
1) u-boot.bin
2) fw_payload.elf

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

This is approximately all the knowledge required for us here.


There are some additional files to consider.
`boot.scr.in` file is processed at build-time to produce a set of
instructions which `u-boot.bin` will execute at run-time.
`gadget.yaml` defines the underlying structure of our Ubuntu Core image.
`fitImage.its` is an optional file in our use case but can be relevant when we
are using a u-boot build in M-mode (spl). This case will require a modified
`snap/snapcraft.yaml` in which we build u-boot twice, once as a payload for
OpenSBI and a second time as a binary containing that `fw_payload.elf`. This is
potentially relevant on *real hardware*.
