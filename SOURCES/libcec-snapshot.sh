#!/bin/bash

tag_name=libcec-3.1.0

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
package=libcec
branch=master
name=libcec

pushd ${tmp}
git clone -b ${tag_name} https://github.com/Pulse-Eight/libcec.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`git describe --tags | awk -F '-' '{print $2}' | tr -d 'v'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}
  

