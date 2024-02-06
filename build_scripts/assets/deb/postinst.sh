#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

ln -s /opt/apple/resources/app.asar.unpacked/daemon/apple /usr/bin/apple || true
ln -s /opt/apple/apple-blockchain /usr/bin/apple-blockchain || true
