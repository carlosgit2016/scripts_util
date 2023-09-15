#!/bin/bash

set -e

file=$(ls -t "/home/cflor/Downloads/" | grep "patching_metrics" | head -n1)
[[ -z "$file" ]] && exit 1
cp -f "/home/cflor/Downloads/$file" .
mv "$file" patching.csv
