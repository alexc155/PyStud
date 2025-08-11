rm -rf build/
rm -rf dist/
nicegui-pack --onefile --name "PyStud" --windowed src/website/main.py
mkdir -p dist/src/database
mkdir -p dist/src/website
cp src/database/*.csv dist/src/database/
cp src/website/*.png dist/src/website/
cp src/website/*.icns dist/PyStud.app/Contents/Resources/