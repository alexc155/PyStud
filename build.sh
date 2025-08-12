#!/bin/sh

rm -rf dist/PyStud.app

python -m PyInstaller PyStud.spec

cp -r PyStud/PyStud.app dist/PyStud.app
mv dist/PyStud dist/PyStud.app/Contents/MacOS/