#!/usr/bin/env bash

sudo kill `ps aux | grep ecat-register | grep -v "grep" | head -3 | awk '{print \$2}'`