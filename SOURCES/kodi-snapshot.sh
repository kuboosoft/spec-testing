#!/bin/bash

tag_name=16.0-Jarvis

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
package=xbmc
branch=master
name=kodi

pushd ${tmp}
git clone -b ${tag_name} --depth 1 https://github.com/xbmc/xbmc.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`git describe --tags | cut -d '-' -f 1`
cd addons
git submodule update --init
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}



