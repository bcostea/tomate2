#!/bin/bash

PREFIX=/usr/local

INSTALLDIR="$PREFIX/share/tomate2"
BINDIR="$PREFIX/bin"

# Are we root?
if [[ $EUID -ne 0 ]]; then
    echo "You must be root to run this script." 2>&1
    exit 1
else
    rm -rf "$INSTALLDIR"
    rm "$BINDIR/tomate2"
    echo "uninstalled tomate2"
fi
