#!/bin/bash

tag_name=rock

set -x

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=rtlwifi_new
branch=rock
name=rtlwifi-firmware-akmod

pushd ${tmp}
git clone -b ${tag_name} https://github.com/lwfinger/${package}.git

cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=1
git archive --prefix="${name}-${version}/" --format=tar rock > "$pwd"/${name}-${version}-${date}-${tag}.tar
bzip2 "$pwd"/${name}-${version}-${date}-${tag}.tar
  

