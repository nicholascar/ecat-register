#!/usr/bin/env bash

# URI file to be altered
U=$1

# base URI to add to IDs
ADD=$2

# add the given URI base to the IDs
sed -i 's|^|'$ADD'|' $U