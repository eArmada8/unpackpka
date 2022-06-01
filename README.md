# unpackpka

Unpacks `.pka` files to `.pkg` files.  Forked from uyjulian/unpackpka, modified for my use.

# Usage

Place extract_pka.py in {Game Folder}/data/asset/D3D11 and run.  First argument in the assets file (defaults to assets.pka).  Second argument is the search term.  If a specific file is requested (e.g. "C_CHR001.pkg"), only that file will be extracted.  If ".pkg" is not included, the argument will be used as a search term (e.g. "C_CHR001" will extract files such as C_CHR001.pkg, C_CHR001_FC1.pkg, FC_CHR001_C02.pkg, etc).  If started without arguments (such as from file explorer), it will start in interactive mode and ask for the names of the files.

# Compatibility

The following games are known to be compatible with this program:  

The Legend of Heroes: Trails of Cold Steel III (PC)

The Legend of Heroes: Trails of Cold Steel IV (PC)

My fork has not been tested with the Switch versions, but the original code states there is compatibility.

# License

The program is licensed under the MIT license. Please check `LICENSE` for more information.
