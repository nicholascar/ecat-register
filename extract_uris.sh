#!/usr/bin/env bash

# XML file to be processed
X=$1

# URI file to be saved
U=$2

# 1. select eCat IDs from XML
sed -n -e 's#^\(.*\)<gco:CharacterString>\([0-9]*\)\(</gco:CharacterString>\)#\2#p' $X > $U

# 2. remove postcodes
sed -i '/2601/d' $U

# 3. sort the IDs
more $U | sort -o $U

# 4.  make URIs
# base URI to add to IDs
ADD=$3

# add the given URI base to the IDs
sed -i 's|^|'$ADD'|' $U
