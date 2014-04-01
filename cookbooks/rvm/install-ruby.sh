#!/usr/bin/env bash


# Check if RVM is already installed
rvm list | grep $1 >/dev/null 2>&1
INSTALLED=$?

# Act on our return value
if [ $INSTALLED == '0' ]; then
	echo "Ruby 1.9.3 is already installed"
else

 source /usr/local/rvm/scripts/rvm

 rvm use --install $1
 rvm --default $1

 shift

 if (( $# ))
 then gem install $@
 fi

fi