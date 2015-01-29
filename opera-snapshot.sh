#!/bin/bash
# Licensed under the GNU General Public License Version 3
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.


ver=$(curl -s http://get.geo.opera.com.global.prod.fastly.net/pub/opera/desktop/ | awk -F '<a href="' '{print $2}' | awk -F '">' '{print $1}' | tr -d '/' | grep '[0-9]' | tail -1)

wait ${!}

if [ `getconf LONG_BIT` = "64" ]; then
libdir=lib64
package=$(curl -s http://get.geo.opera.com.global.prod.fastly.net/pub/opera/desktop/$ver/linux/ | grep 'amd64' | awk -F '<a href="' '{print $2}' | awk -F '">' '{print $1}') 
else
libdir=lib
package=$(curl -s http://get.geo.opera.com.global.prod.fastly.net/pub/opera/desktop/$ver/linux/ | grep 'i386' | awk -F '<a href="' '{print $2}' | awk -F '">' '{print $1}')
fi 

Architecture=$(uname -m)

Source="http://get.geo.opera.com.global.prod.fastly.net/pub/opera/desktop/$ver/linux/$package"

wait ${!}


echo '=> Downloading sources'
wget -c -P ~/rpmbuild/SOURCES/ $Source
wget -c -P ~/rpmbuild/SOURCES  http://mirrors.kernel.org/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.1f-1ubuntu2.8_amd64.deb
