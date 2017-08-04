#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SARC Packer
# Version v0.1
# Copyright © 2017 Stella/AboodXD

import os
import sys
import time

import SARC

def pack(root, endianness, padding, outname):
    """
    Pack the files and folders in the root folder.
    """
    
    arc = SARC.SARC_Archive(endianness=endianness)

    print("")
    
    for path, dirs, files in os.walk(root):
        if "\\" in path:
            path = "/".join(path.split("\\")[1:])
        elif "/":
            path = "/".join(path.split("/")[1:])

        for file in files:
            if path != "":
                filename = path + "/" + file
            else:
                filename = file

            print(filename)

            fullname = root + "/" + filename

            i = 0
            for folder in filename.split("/")[:-1]:
                if i == 0:
                    exec("folder%i = SARC.Folder(folder + '/'); arc.addFolder(folder%i)".replace('%i', str(i)))
                else:
                    exec("folder%i = SARC.Folder(folder + '/'); folder%m.addFolder(folder%i)".replace('%i', str(i)).replace('%m', str(i-1)))
                i += 1

            with open(fullname, "rb") as f:
                inb = f.read()

            if i == 0:
                arc.addFile(SARC.File(file, inb))
            else:
                exec("folder%m.addFile(SARC.File(file, inb))".replace('%m', str(i-1)))

    data = arc.save(padding)

    if not outname:
        if root.endswith("\\"):
            root = root[:-2]
        elif root.endswith("/"):
            root = root[:-1]

        outname = root + ".sarc"

    with open(outname, "wb+") as output:
        output.write(data)


def printInfo():
    print("")
    print("Usage:")
    print("  main [option...] folder")
    print("")
    print("Options:")
    print(" -o <output>     output file (Optional)")
    print(" -bom <bom>      endiannes (Optional)")
    print(" -padd <padd>    padding value (Optional)")
    print("")
    print("bom:")
    print("0 - Big Endain (Wii U)")
    print("1 - Little Endian (3DS/Switch)")
    print('')
    print("Exiting in 5 seconds...")
    time.sleep(5)
    sys.exit(1)


def main():
    print("SARC Packer v0.1")
    print("(C) 2017 Stella/AboodXD")
    print("Special thanks to Reggie! Next team!")

    if len(sys.argv) < 2:
        printInfo()
    
    if os.path.isdir(sys.argv[-1]):
        root = sys.argv[-1]
    else:
        printInfo()

    if "-bom" in sys.argv:
        bom = int(sys.argv[sys.argv.index("-bom") + 1], 0)
    else:
        bom = 0

    if "-padd" in sys.argv:
        padding = int(sys.argv[sys.argv.index("-padd") + 1], 0)
    else:
        padding = 0x2000

    if "-o" in sys.argv:
        outname = sys.argv[sys.argv.index("-o") + 1]
    else:
        outname = ""

    if bom > 1:
        printInfo()

    if bom == 0:
        endianness = '>'
    else:
        endianness = '<'

    pack(root, endianness, padding, outname)

if __name__ == '__main__': main()
