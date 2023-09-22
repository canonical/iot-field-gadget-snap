#!/bin/sh

set -x

mkdir -p $SNAP_COMMON
exec >> $SNAP_COMMON/prepare-device-hook.log 2>&1

export PATH=$PATH:$SNAP/usr/bin

serial=$(uuidgen)

# Set the serial number of the device (needed for the serial assertion)
snapctl set registration.proposed-serial="\"${serial}\""

# Set the location of the Serial Vault and the API key
snapctl set device-service.url="<<<MODEL_APIURL>>>"
snapctl set device-service.headers='{"api-key": "<<<MODEL_APIKEY>>>"}'
