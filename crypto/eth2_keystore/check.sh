#!/usr/bin/env bash

set -o errexit

# Workaround to avoid multiple workspaces
rm -f Cargo.toml

# Go to eth2_keystore
cd ..

# Check that this version of the crate actually compiles
cargo check || exit 125

# Run the check
cargo run --release --bin test_keystore

# Put the Cargo.toml back
cd block-ciphers
git checkout HEAD Cargo.toml
