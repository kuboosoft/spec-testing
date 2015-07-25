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
date=$(date +%Y%m%d)
package=pencil
branch=master
name=pencil2d

pushd ${tmp}
git clone https://github.com/pencil2d/${package}.git
cd ${package}/
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=0.5.5
git archive --prefix="${name}-${version}/" --format=tar master > "$pwd"/${name}-${version}-${date}-${tag}.tar
  
