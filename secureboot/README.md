# Enabling SecureBoot for u-boot systems

One of the most important features in the modern era is full disk encryption
(FDE). Ubuntu Core treats this feature as a first class citizen on sufficiently
compliant x86_64 hardware (for instance, TPM 2.0 support), but supporting FDE on
alternative architectures proves to be a bit more involved.

FDE is only enabled on Ubuntu Core just in case SecureBoot (SB) is enabled, to
ensure the integrity of the boot chain. This means that FDE is only available on
platforms where SB is supported.

Ubuntu Core's reference implementation for SecureBoot on ARM platforms is an
OP-TEE-based mechanism. If OP-TEE supports the target platform, it's quite
possible that some tweaks can be done to the boot chain and the gadget snap to
enable SB and FDE for the platform!

This directory includes two things:


1) A `patches/` directory

This directory contains a collection of patches which can be used as a
**reference** for not only some robust settings for Ubuntu Core systems in
general, but also to ensure SB can be used.

The actual implementation details for how this works on a platform is up to the
individual device manufacturer (or even a prolific hobbyist). The `patches/
` directory includes an example for how this could be implemented for the NXP
i.MX8MM platform.

These patches should be applied to the u-boot part in the `snapcraft.yaml`.
In the context of this particular branch, these patches would be added to
`u-boot-src.override-pull`.

These patches are based on the efforts of Ondrej Kubik. That work can be found
[here](https://git.launchpad.net/~ondrak/+git/u-boot/tree/?h=lf_v2023.04-uc)
starting from commit 2e71f4422c312e7afefd3bed6dda7e10fd1d4ace.


2) Extensions to the snap project files

The [`snap/snapcraft.yaml`](snap/snapcraft.yaml) includes snippets which should
be added to the parent [`snapcraft.yaml`](../snap/snapcraft.yaml) to include all
of the bits required of the gadget snap for snapd to handle the relevant things
for enabling SB and FDE.

A new `pkcs/` directory adds some useful helper scripts.

An additional hook [`snap/hooks/connect-plug-tee`](snap/hooks/connect-plug-tee)
to start and enable the relevant apps when the [`tee`](https://snapcraft.io/docs/tee-interface) 
interface has been connected.


Again, this is likewise just a **reference**; the way in which this is handled
can be quite varied and is entirely up to the device manufacturer.
