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
package=qmltermwidget
branch=master
name=qmltermwidget

pushd ${tmp}
git clone https://github.com/Swordfish90/${package}.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`curl -k https://github.com/Swordfish90/qmltermwidget/ | grep '/Swordfish90/qmltermwidget/tree/v[0-9]' | awk '{print $2}' | awk -F'v' '{print $2}'| sed 's/"//' | sort | sed '/^\s*$/d' | tail -1`
git archive --prefix="${name}-${version}/" --format=tar master > "$pwd"/${name}-${version}-${date}-${tag}.tar
  
