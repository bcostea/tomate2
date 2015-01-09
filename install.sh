#!/bin/bash

PREFIX=/usr/local

INSTALLDIR="$PREFIX/share/tomate2"
BINDIR="$PREFIX/bin"

# Are we root?
if [[ $EUID -ne 0 ]]; then
    echo "You must be root to run this script." 2>&1
    exit 1
else
    mkdir -p "$INSTALLDIR"
    cp -r . "$INSTALLDIR/"
    echo "Installed tomate2 to $INSTALLDIR"
    ln -s "$INSTALLDIR/tomate2.py" "$BINDIR/tomate2"
    echo "tomate2 start the app"
fi
