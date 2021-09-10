#!/usr/bin/python
import glob 
import subprocess

files = glob.glob("./systemAPPS/*")

for filename in files:
    print filename

