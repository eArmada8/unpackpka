# Script to extract specific .pkg files from assets.pka, tested in Trails of Cold Steel 3/4.  Place in the
# {game}\data\asset\D3D11 folder and execute.  If no arguments are passed, it will start in interactive mode.
# syntax: python3 extract_pka.py assets.pka PKG_FILE_TO_EXTRACT
# If PKG_FILE_TO_EXTRACT is a specific filename (case-sensitive), it will only extract that filename.
# If PKG_FILE_TO_EXTRACT is part of a filename, it will do a search and extract all matches.
# GitHub eArmada8/unpackpka, forked from uyjulian/unpackpka 

import sys
import os
import struct

# Set current directory
os.chdir(os.path.abspath(os.path.dirname(__file__)))

try:
    asset_file = sys.argv[1]
    if not os.path.exists(asset_file):
        raise Exception('Error: Asset archive "' + asset_file + '" does not exist!')
except IndexError:
    asset_file = str(input("Please enter the name of assets archive: [default: assets.pka]  ") or "assets.pka")
    while not os.path.exists(asset_file):
        asset_file = str(input("File does not exist.  Please enter the name of assets archive: [default: assets.pka]  ") or "assets.pka")

with open(asset_file, "rb") as f:
    pka_header, = struct.unpack("<I", f.read(4))
    if pka_header != 0x7FF7CF0D:
        raise Exception("This isn't a pka file")
    total_package_entries, = struct.unpack("<I", f.read(4))
    package_entries = {}
    for _ in range(total_package_entries):
        package_name, number_files = struct.unpack("<32sI", f.read(32+4))
        file_entries = []
        for _ in range(number_files):
            file_entry_name, file_entry_hash = struct.unpack("<64s32s", f.read(64+32))
            file_entries.append([file_entry_name.rstrip(b"\x00"), file_entry_hash])
        package_entries[package_name.rstrip(b"\x00").decode("ASCII")] = file_entries
    total_file_entries, = struct.unpack("<I", f.read(4))
    file_entries = {}
    for _ in range(total_file_entries):
        file_entry_hash, file_entry_offset, file_entry_compressed_size, file_entry_uncompressed_size, file_entry_flags = struct.unpack("<32sQIII", f.read(32+8+4+4+4))
        file_entries[file_entry_hash] = [file_entry_offset, file_entry_compressed_size, file_entry_uncompressed_size, file_entry_flags]

    try:
        package_filter = sys.argv[2]
    except IndexError:    
        package_filter = str(input("Please enter the name of package to extract: [partial matches allowed, case sensitive, .pkg indicates exact match only]  "))
    if not package_filter[-4:] == '.pkg':
        packages_to_extract = dict(filter(lambda item: package_filter in item[0], package_entries.items()))
    else:
        packages_to_extract = dict(filter(lambda item: package_filter == item[0], package_entries.items()))
        
    for package_name in packages_to_extract.keys():
        package_file_entries = package_entries[package_name]
        rebased_package_file_entries = {}
        rebased_file_entry_start = 8 + ((64+4+4+4+4) * len(package_file_entries))
        for file_entry in package_file_entries:
            rebased_file_entry = list(file_entries[file_entry[1]]) # clone the list
            rebased_file_entry.append(rebased_file_entry_start) # append the new offset
            rebased_file_entry_start += rebased_file_entry[1]
            rebased_package_file_entries[file_entry[0]] = rebased_file_entry
        if not os.path.exists(package_name):
            with open(package_name, "wb") as wf:
                wf.write(b"\x00\x00\x00\x00")
                wf.write(struct.pack("<I", len(package_file_entries)))
                for file_entry_name in rebased_package_file_entries.keys():
                    file_entry = rebased_package_file_entries[file_entry_name]
                    wf.write(struct.pack("<64sIIII", file_entry_name, file_entry[2], file_entry[1], file_entry[4], file_entry[3]))
                for file_entry_name in rebased_package_file_entries.keys():
                    file_entry = rebased_package_file_entries[file_entry_name]
                    f.seek(file_entry[0])
                    wf.write(f.read(file_entry[1])) # Copy data
