#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SARC Packer
# Version v0.3
# Copyright © 2017-2018 MasterVermilli0n / AboodXD

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################
################################################################

import os
import sys
import time

import SARC

def pack(root, endianness, dataStart, outname):
    """
    Pack the files and folders in the root folder.
    """

    if "\\" in root:
        root = "/".join(root.split("\\"))

    if root[-1] == "/":
        root = root[:-1]

    arc = SARC.SARC_Archive(endianness=endianness)
    lenroot = len(root.split("/"))

    for path, dirs, files in os.walk(root):
        if "\\" in path:
            path = "/".join(path.split("\\"))

        lenpath = len(path.split("/"))

        if lenpath == lenroot:
            path = ""

        else:
            path = "/".join(path.split("/")[lenroot - lenpath:])

        for file in files:
            if path:
                filename = ''.join([path, "/", file])

            else:
                filename = file

            print(filename)

            fullname = ''.join([root, "/", filename])

            i = 0
            for folder in filename.split("/")[:-1]:
                if not i:
                    exec("folder%i = SARC.Folder(folder + '/'); arc.addFolder(folder%i)".replace('%i', str(i)))

                else:
                    exec("folder%i = SARC.Folder(folder + '/'); folder%m.addFolder(folder%i)".replace('%i', str(i)).replace('%m', str(i - 1)))

                i += 1

            with open(fullname, "rb") as f:
                inb = f.read()

            if not i:
                arc.addFile(SARC.File(file, inb))

            else:
                exec("folder%m.addFile(SARC.File(file, inb))".replace('%m', str(i - 1)))

    data = arc.save(dataStart)

    if not outname:
        outname = ''.join([root, ".sarc"])

    with open(outname, "wb+") as output:
        output.write(data)


def printInfo():
    print("Usage:")
    print("  main [option...] folder")
    print("\nOptions:")
    print(" -o <output>           output file name (Optional)")
    print(" -little               output will be in little endian if this is used")
    print(" -dataStart <value>    beginning of data offset (Optional)")
    print("                       this option excepts decimal, hex, and binary values")
    print("Exiting in 5 seconds...")
    time.sleep(5)
    sys.exit(1)


def main():
    print("SARC Packer v0.3")
    print("(C) 2017-2018 MasterVermilli0n / AboodXD")
    print("Thanks to RoadrunnerWMC for original SARC code\n")

    if len(sys.argv) < 2:
        printInfo()

    root = sys.argv[-1]
    if not os.path.isdir(root):
        printInfo()

    if "-bom" in sys.argv:
        endianness = '<'

    else:
        endianness = '>'

    if "-dataStart" in sys.argv:
        try:
            dataStart = int(sys.argv[sys.argv.index("-dataStart") + 1], 0)

        except ValueError:
            dataStart = 0x100

    else:
        dataStart = 0x100

    if "-o" in sys.argv:
        outname = sys.argv[sys.argv.index("-o") + 1]

    else:
        outname = ""

    pack(root, endianness, dataStart, outname)

if __name__ == '__main__': main()
