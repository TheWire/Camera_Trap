#!/usr/bin/env bash
cd ./frontend
npm run build
rm -r ../static
cp -r ./build/static ../
mkdir -p ../templates
cp ./build/index.html ../templates