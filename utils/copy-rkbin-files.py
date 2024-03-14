#!/usr/bin/env python3

import sys
import os
import shutil
import configparser

RKTRUST="RK3588TRUST.ini"
RKBOOT="RK3588MINIALL.ini"
BL31="rk3588_bl31.elf"
BL32="rk3588_bl32.bin"
DDR="rk3588_ddr.bin"

def read_ini(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def copy_file(source: str, target: str):
    print(f"Copying {source} to {target}")
    target_dir = os.path.dirname(target)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    shutil.copyfile(source, target)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path to rkbin> <target>")
        sys.exit(1)

    rkbin_path = sys.argv[1]
    target_path = sys.argv[2]
    rktrust = read_ini(os.path.join(rkbin_path, "RKTRUST", RKTRUST))
    rkboot = read_ini(os.path.join(rkbin_path, "RKBOOT", RKBOOT))

    ddr = rkboot["LOADER_OPTION"]["FlashData"]
    bl31 = rktrust["BL31_OPTION"]["PATH"]
    bl32 = rktrust["BL32_OPTION"]["PATH"]

    copy_file(os.path.join(rkbin_path,ddr), os.path.join(target_path, DDR))
    copy_file(os.path.join(rkbin_path,bl31), os.path.join(target_path, BL31))
    copy_file(os.path.join(rkbin_path,bl32), os.path.join(target_path, BL32))

if __name__ == "__main__":
    main()
