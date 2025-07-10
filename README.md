# IoT Field Gadget Snaps

This repository is maintained by the IoT Devices Field team to store and test
gadget snaps we create.

If you are looking for Canonical reference gadget snaps, please see [this](https://github.com/snapcore/pc-gadget) repository.

Note that the contents of these gadget snaps are all public information and are
generally created for testing or interest in particular hardware. No promises
are made for stability or long term support.

Gadget snaps are generally verboten from the Global Store, so you will not
find these published anywhere. They are intended as implementation examples and
inspiration, for use on dangerous-grade model Ubuntu Core images.

* You can find IoT Field's kernel snaps [at this sister repository](https://github.com/canonical/iot-field-kernel-snap)
* You can find IoT Field's example snaps [at this cousin repository](https://github.com/canonical/iot-field-example-snaps)


## Repository structure

The branches correspond to a Core release and any platforms which hhave had a
gadget snap made for them can be found in that branch under their respective
subdirectory.

* The `main` branch is for hosting workflows, a project description (this
README), and an example skeleton of a gadget snap.
* If you wish to add a new gadget to this repository, create a subdirectory for
the platform on the relevant branch.
* If the gadget snap is one for Classic systems, please add a `-classic` suffix
to the directory name.
* If you wish to update a kernel snap from one base to another, please switch
to the branch corresponding to the targetted release and checkout the platform's
subdirectory from the most recent branch. For example:

```sh
  git checkout 24
  git checkout 22 -- nezha
  # proceed
```


## Subdirectories

Please ensure that your subdirectory includes a README describing:
  - the board,
  - how the gadget functions (in broad, general terms; no need to be too technical),
  - including references to documentation if you prefer


## Workflows

The expectation is that any new subdirectory should have an accompanying new
workflow added. That workflow should follow the general style of the other
workflows, and ideally there are two:

1) One workflow testing builds using some version-specific snapcraft (e.g. `7.x/edge`)
2) One workflow testing builds using snapcraft from `latest/edge`

This ensures continuous testing of our work to spot any potential regressions or breaking changes.

The workflows should only exist on the `main` branch.


## Contributing

This repository is open to contributions so long as:

1) You have signed the Canonical [Contributor License Agreement](https://ubuntu.com/legal/contributors)
2) You have signed the Ubuntu [Code of Conduct](https://launchpad.net/codeofconduct)


Commits should follow the below style:

* The entire message should read as:

```
    <path/to/file>: <imperative present tense short description of change>

    <longer explanation of change if required>

    Signed-off-by: <author name> <author email>
```

* Keep first line summaries to under 60 characters, body summaries under 80

* Include a signoff for each commit using `git commit -s`
    * To amend prior commits with a signoff, do `git rebase --signoff HEAD~<number of commits>`

* Signing commits with `git commit -S` (GPG or SSH) is preferred but not required

* If you are modifying the `README.md`, `LICENSE`, `.gitignore`, `.github`,
    etc., please use `README`, `LICENSE`, `github`, `gitignore`, etc as the filename in the message

* Commits should be atomic

* PRs should contain logically related commits

* Try to follow prior art and style wherever possible


Even if you have write permissions to this repository, unless it is trivial
please create a PR for your change and attempt to get a +1 from someone on the
FE IoT team.


## Debugging

When building Ubuntu Core images, especially for hardware for which no Ubuntu
Core image currently exists, having some debugging tactics ready can prove very
useful.


### u-boot

u-boot behavior can vary greatly depending on the hardware being targeted. The
best rule of thumb is to always defer to the board manufacturer's documentation.
If that fails, I've always found that other hobbyists can prove indispensible
resources :)

One big issue you may discover is that the objects you are trying to load into
memory to boot are larger than some available region. You'll frequently see this
is the case if you have both a small amount of RAM and an inordinately large
kernel binary or ramdisk. Beyond trying to make those objects smaller, you can
always explore what memory is free using traditionally built-in u-boot tools,
such as `md` and `bdi`. Once you find a large enough region of memory, update
the (usually) `$kernel_addr_r`, `$ramdisk_addr_r`, and `$fdt_addr_r` in the
u-boot env.


### General runtime

There are a few handy tools available when it comes to debugging the general
runtime of your Ubuntu Core system. If you're doing a board bringup on some
hardware for the first time, having this tricks available can dramatically
improve your success rates.

One primary tool for improving the debugability of your Ubuntu Core image is
extending the kernel commandline parameters, as these allow you to directly tell
snapd and systemd how to handle the boot process without mangling your initrd or
userspace. The gadget snap is a prime place for doing this work, as part of its
job is adding kernel commandline arguments to the boot process!

Here are some useful kernel commandline options, some Ubuntu Core specific and
others generally applicable:

| Argument                               | Effect                                         |
| -------------------------------------- | ---------------------------------------------- |
|dangerous                               |unmask services which drop to recovery shell    |
|snapd.debug=1                           |Tells snapd to provide more output              |
|systemd.debug-shell=ttyS0               |Create a debug shell on the specified TTY       |
|systemd.journald.forward_to_console=1   |Output more device status/logging               |
|rd.systemd.journald.forward_to_console=1|Output more device status/logging, in the initrd|

If booting a u-boot system, you can add these to something like a `boot.scr`
script, see [here](https://github.com/canonical/iot-field-gadget-snap/blob/01c59d8dedc08adc91929b7b519886f7fa53aa4b/u-boot/boot.scr.in#L64).

If booting an AMD64 system using GRUB, you can add these to a `cmdline.extra`
or `cmdline.full` file in the root of the gadget snap for snapd to pickup on and
use. For instance, check the handling and contents of the `extra` directory
[here](https://github.com/canonical/pc-amd64-gadget-desktop/tree/24).
