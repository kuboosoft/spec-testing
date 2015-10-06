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
package=Kvantum
branch=master
name=kvantum

pushd ${tmp}
git clone https://github.com/tsujan/${package}.git
cd ${package}/${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=$(cat ChangeLog | grep "V[0-9]" | awk -F'V' '{print $2}' | sort | sed '/^\s*$/d' | tail -1 )
git archive --prefix="${name}-${version}/" --format=tar master > "$pwd"/${name}-${version}-${date}-${tag}.tar
  
