#!/bin/bash

set -x

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
amdname=amd-catalyst-omega
version=14.12
ZIPFILE="amd-catalyst-omega-14.12-linux-run-installers.zip"
AMDDOWNLOADURL="http://www2.ati.com/drivers/linux/${ZIPFILE}"

pushd ${tmp}
curl -f -A "Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0" -e "http://support.amd.com/de-de/download/desktop?os=Linux+x86" -o "${ZIPFILE}" "${AMDDOWNLOADURL}"
