#!/bin/bash

. ${HOME}/etc/shell.conf
echo $LG_FRAMES | awk '{print $1}'