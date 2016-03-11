#!/bin/bash

tag_name=platform-2.0.1
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
package=platform
name=platform

pushd ${tmp}
git clone -b ${tag_name} https://github.com/Pulse-Eight/platform.git
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`echo $tag_name | awk -F 'platform-' '{print $2}' | tr -d 'v'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}



