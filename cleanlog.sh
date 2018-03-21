#!/usr/bin/bash
# clean.sh

find . -name "*.log" | xargs rm -f
find . -regex ".*[0-9]\.[0-9].*txt" | xargs rm -f