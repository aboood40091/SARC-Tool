#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SARC Tool
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

try:
    import SarcLib

except ImportError:
    print("SarcLib is not installed!")
    ans = input("Do you want to install it now? (y/n)\t")
    if ans.lower() == 'y':
        import pip
        pip.main(['install', 'SarcLib==0.1'])
        del pip

        import SarcLib

    else:
        sys.exit(1)

try:
    import libyaz0

except ImportError:
    print("libyaz0 is not installed!")
    ans = input("Do you want to install it now? (y/n)\t")
    if ans.lower() == 'y':
        import pip
        pip.main(['install', 'libyaz0==0.5'])
        del pip

        import libyaz0

    else:
        sys.exit(1)


def extract(file):
    """
    Extrct the given archive
    """
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(file)[0]
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(''.join([name, ext]), "wb") as out:
            out.write(inb)

    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(os.path.dirname(os.path.abspath(file)), name)
        if not os.path.isdir(root):
            os.mkdir(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal files

            for checkObj in folder:
                if isinstance(checkObj, SarcLib.File):
                    files.append(["/".join([path, checkObj.name]), checkObj.data])

                else:
                    getAbsPath(checkObj, "/".join([path, checkObj.name]))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])

            else:
                getAbsPath(checkObj, checkObj.name)

        for file, fileData in files:
            print(file)
            with open(os.path.join(root, file), "wb") as out:
                out.write(fileData)


def pack(root, endianness, dataStartOffset, level, outname):
    """
    Pack the files and folders in the root folder.
    """

    if "\\" in root:
        root = "/".join(root.split("\\"))

    if root[-1] == "/":
        root = root[:-1]

    arc = SarcLib.SARC_Archive(endianness=endianness)
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
                    exec("folder%i = SarcLib.Folder(folder + '/'); arc.addFolder(folder%i)".replace('%i', str(i)))

                else:
                    exec("folder%i = SarcLib.Folder(folder + '/'); folder%m.addFolder(folder%i)".replace('%i', str(i)).replace('%m', str(i - 1)))

                i += 1

            with open(fullname, "rb") as f:
                inb = f.read()

            hasFilename = True
            if file[:5] == "hash_":
                hasFilename = False

            if not i:
                arc.addFile(SarcLib.File(file, inb, hasFilename))

            else:
                exec("folder%m.addFile(SarcLib.File(file, inb, hasFilename))".replace('%m', str(i - 1)))

    data, maxAlignment = arc.save(dataStartOffset)

    if level != -1:
        outData = libyaz0.compress(data, maxAlignment, level)
        del data

        if not outname:
            outname = ''.join([root, ".szs"])

    else:
        outData = data
        if not outname:
            outname = ''.join([root, ".sarc"])

    with open(outname, "wb+") as output:
        output.write(outData)


def printInfo():
    print("Usage:")
    print("  main [option...] file/folder")
    print("\nPacking Options:")
    print(" -o <output>           output file name (Optional)")
    print(" -little               output will be in little endian if this is used")
    print(" -compress <level>     Yaz0 (SZS) compress the output with the specified level(0-9) (1 is the default)")
    print("                       0: No compression (Fastest)")
    print("                       9: Best compression (Slowest)")
    print("\nExiting in 5 seconds...")
    time.sleep(5)
    sys.exit(1)


def main():
    print("SARC Tool v0.3")
    print("(C) 2017-2018 MasterVermilli0n / AboodXD\n")

    if len(sys.argv) < 2:
        printInfo()

    root = sys.argv[-1]
    if os.path.isfile(root):
        extract(root)

    elif os.path.isdir(root):
        endianness = '>'
        dataStartOffset = 0
        level = -1

        if "-little" in sys.argv:
            endianness = '<'

        if "-dataStart" in sys.argv:
            try:
                dataStartOffset = int(sys.argv[sys.argv.index("-dataStart") + 1], 0)

            except ValueError:
                pass

        if "-compress" in sys.argv:
            try:
                level = int(sys.argv[sys.argv.index("-compress") + 1], 0)

            except ValueError:
                level = 1

            if not 0 <= level <= 9:
                print("Invalid compression level!\n")
                print("Exiting in 5 seconds...")
                time.sleep(5)
                sys.exit(1)

        if "-o" in sys.argv:
            outname = sys.argv[sys.argv.index("-o") + 1]

        else:
            outname = ""

        pack(root, endianness, dataStartOffset, level, outname)

    else:
        print("File/Folder doesn't exist!")
        print("\nExiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

if __name__ == '__main__': main()
