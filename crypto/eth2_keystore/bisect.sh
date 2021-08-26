#!/usr/bin/env bash

set -o errexit

if [ -z "$PASSWORD" ]
then
    echo "Please define keystore password in \$PASSWORD env variable"
    exit 1
fi

if [ ! -f keystore.json ]
then
    echo "Please place faulty keystore in current directory, named 'keystore.json'"
    exit 1
fi

# Check out block-ciphers
git submodule init
git submodule update

# Start bisection
cd block-ciphers
git bisect start aes-v0.7.4 aes-v0.6.0

# Run the checker script
git bisect run ../check.sh
