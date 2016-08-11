#!/usr/bin/env bash
LINES=$1
REMOVED_FROM=$2
RESULT=$3

awk '{if (f==1) { r[$0] } else if (! ($0 in r)) { print $0 } } ' f=1 $LINES f=2 $REMOVED_FROM > $RESULT