#!/bin/bash

cd $(dirname "$0")

version=$(python -c 'import json; print json.load(open("src/manifest.json", "r"))["version"]')
filename="datahack-floor19-talkbacker-chrome-ext.${version}.zip"
rm -f "dist/${filename}"

# merge a few local files
zip "dist/${filename}" LICENSE README.md
# with all the src files recursively, stripping off the 'src/' prefix
cd src
zip -r "../dist/${filename}" ./*
cd ..

