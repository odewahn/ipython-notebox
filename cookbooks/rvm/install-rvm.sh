#!/usr/bin/env bash

# Check if RVM is already installed
rvm --version >/dev/null 2>&1
INSTALLED=$?

# Act on our return value
if [ $INSTALLED == '0' ]; then
	echo "RVM is already installed"
else
   curl -sSL https://get.rvm.io | bash -s $1
fi