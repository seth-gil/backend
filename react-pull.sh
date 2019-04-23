#!/bin/bash

cd /home/ec2-user/app/root
rm -rf ./build ./precache-manifest* ./manifest.json ./asset-manifest.json ./static
svn export https://github.com/seth-gil/frontend/trunk/build
mv ./build/* ./