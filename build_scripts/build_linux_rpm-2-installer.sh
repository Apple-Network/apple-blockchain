#!/bin/bash

set -o errexit

git status
git submodule

if [ ! "$1" ]; then
  echo "This script requires either amd64 of arm64 as an argument"
	exit 1
elif [ "$1" = "amd64" ]; then
	export REDHAT_PLATFORM="x86_64"
else
	export REDHAT_PLATFORM="arm64"
fi

# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG

if [ ! "$APPLE_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable APPLE_INSTALLER_VERSION set. Using 0.0.0."
	APPLE_INSTALLER_VERSION="0.0.0"
fi
echo "Apple Installer Version is: $APPLE_INSTALLER_VERSION"

echo "Installing npm and electron packagers"
cd npm_linux || exit 1
npm ci
cd .. || exit 1

echo "Create dist/"
rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
SPEC_FILE=$(python -c 'import sys; from pathlib import Path; path = Path(sys.argv[1]); print(path.absolute().as_posix())' "pyinstaller.spec")
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi

# Creates a directory of licenses
echo "Building pip and NPM license directory"
pwd
bash ./build_license_directory.sh

# Builds CLI only rpm
CLI_RPM_BASE="apple-blockchain-cli-$APPLE_INSTALLER_VERSION-1.$REDHAT_PLATFORM"
mkdir -p "dist/$CLI_RPM_BASE/opt/apple"
mkdir -p "dist/$CLI_RPM_BASE/usr/bin"
mkdir -p "dist/$CLI_RPM_BASE/etc/systemd/system"
cp -r dist/daemon/* "dist/$CLI_RPM_BASE/opt/apple/"
cp assets/systemd/*.service "dist/$CLI_RPM_BASE/etc/systemd/system/"

ln -s ../../opt/apple/apple "dist/$CLI_RPM_BASE/usr/bin/apple"
# This is built into the base build image
# shellcheck disable=SC1091
. /etc/profile.d/rvm.sh
rvm use ruby-3
# /usr/lib64/libcrypt.so.1 is marked as a dependency specifically because newer versions of fedora bundle
# libcrypt.so.2 by default, and the libxcrypt-compat package needs to be installed for the other version
# Marking as a dependency allows yum/dnf to automatically install the libxcrypt-compat package as well
fpm -s dir -t rpm \
  -C "dist/$CLI_RPM_BASE" \
  --directories "/opt/apple" \
  -p "dist/$CLI_RPM_BASE.rpm" \
  --name apple-blockchain-cli \
  --license Apache-2.0 \
  --version "$APPLE_INSTALLER_VERSION" \
  --architecture "$REDHAT_PLATFORM" \
  --description "Apple is a modern cryptocurrency built from scratch, designed to be efficient, decentralized, and secure." \
  --rpm-tag 'Recommends: libxcrypt-compat' \
  --rpm-tag '%define _build_id_links none' \
  --rpm-tag '%undefine _missing_build_ids_terminate_build' \
  --before-install=assets/rpm/before-install.sh \
  --rpm-tag 'Requires(pre): findutils' \
  .
# CLI only rpm done
cp -r dist/daemon ../apple-blockchain-gui/packages/gui
# Change to the gui package
cd ../apple-blockchain-gui/packages/gui || exit 1

# sets the version for apple-blockchain in package.json
cp package.json package.json.orig
jq --arg VER "$APPLE_INSTALLER_VERSION" '.version=$VER' package.json > temp.json && mv temp.json package.json

echo "Building Linux(rpm) Electron app"
OPT_ARCH="--x64"
if [ "$REDHAT_PLATFORM" = "arm64" ]; then
  OPT_ARCH="--arm64"
fi
PRODUCT_NAME="apple"
echo npx electron-builder build --linux rpm "${OPT_ARCH}" \
  --config.extraMetadata.name=apple-blockchain \
  --config.productName="${PRODUCT_NAME}" --config.linux.desktop.Name="Apple Blockchain" \
  --config.rpm.packageName="apple-blockchain"
npx electron-builder build --linux rpm "${OPT_ARCH}" \
  --config.extraMetadata.name=apple-blockchain \
  --config.productName="${PRODUCT_NAME}" --config.linux.desktop.Name="Apple Blockchain" \
  --config.rpm.packageName="apple-blockchain"
LAST_EXIT_CODE=$?
ls -l dist/linux*-unpacked/resources

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-builder failed!"
	exit $LAST_EXIT_CODE
fi

GUI_RPM_NAME="apple-blockchain-${APPLE_INSTALLER_VERSION}-1.${REDHAT_PLATFORM}.rpm"
mv "dist/${PRODUCT_NAME}-${APPLE_INSTALLER_VERSION}.rpm" "../../../build_scripts/dist/${GUI_RPM_NAME}"
cd ../../../build_scripts || exit 1

echo "Create final installer"
rm -rf final_installer
mkdir final_installer

mv "dist/${GUI_RPM_NAME}" final_installer/
# Move the cli only rpm into final installers as well, so it gets uploaded as an artifact
mv "dist/$CLI_RPM_BASE.rpm" final_installer/

ls -l final_installer/
