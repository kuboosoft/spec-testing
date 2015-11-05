#global buildforkernels newest
%global buildforkernels current
#global buildforkernels akmod

Name:               rtlwifi-firmware-kmod
Version:            1
Release:     	    1%{?dist}
Summary:            rtlwifi kernel modules
Source0:            rtlwifi-firmware-akmod-1-20150917-f8711b8.tar.bz2
Source1:	    rtlwifi-firmware-akmod-snapshot.sh	
Source11:           excludekernel-filterfile
URL:                https://github.com/lwfinger/rtlwifi_new
Group:              System Environment/Kernel
License:	    Freeware
BuildRequires:      %{_bindir}/kmodtool

ExclusiveArch:      i686 x86_64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the rtlwifi wireless firmware files
rtl8192ce, rtl8192se, rtl8192de, rtl8188ee, rtl8192ee, rtl8723ae, rtl8723be, and rtl8821ae.

%package -n	rtlwifi-firmware
Summary:	rtlwifi userland package
Requires: %{name}-kmod  >= %{version}
Provides: %{name}-kmod-common = %{version}
%description -n rtlwifi-firmware
userland package for more details http://rpmfusion.org/Packaging/KernelModules/Kmods2#userland_package

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
# pushd foo-%{version}
# #patch0 -p1 -b .suffix
# popd

for kernel_version in %{?kernel_versions} ; do
    cp -a rtlwifi-firmware-akmod-1 _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} -C ${kernel_version##*___} M=`pwd` modules
    popd
#    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done



%install
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/btcoexist
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8188ee
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192c
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192ce
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192cu
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192de
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192ee
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192se
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8723ae
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8723be
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8821ae
 install -p -D -m 644 rtl_pci.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -p -D -m 644 rtl_usb.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -p -D -m 644 rtlwifi.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -p -D -m 644 ./btcoexist/btcoexist.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/btcoexist
 install -p -D -m 644 ./rtl8188ee/rtl8188ee.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8188ee
 install -p -D -m 644 ./rtl8192c/rtl8192c-common.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192c
 install -p -D -m 644 ./rtl8192ce/rtl8192ce.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192ce
 install -p -D -m 644 ./rtl8192cu/rtl8192cu.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192cu
 install -p -D -m 644 ./rtl8192de/rtl8192de.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192de
 install -p -D -m 644 ./rtl8192ee/rtl8192ee.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192ee
 install -p -D -m 644 ./rtl8192se/rtl8192se.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8192se
 install -p -D -m 644 ./rtl8723ae/rtl8723ae.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8723ae
 install -p -D -m 644 ./rtl8723be/rtl8723be.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8723be
 install -p -D -m 644 ./rtl8821ae/rtl8821ae.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}/rtl8821ae
 #make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 popd
done
%{?akmod_install}


%files -n rtlwifi-firmware

%changelog
* Sat Sep 12 2015 David Vasquez <davidjeremias82 at gmail dot com> - 1-1
- Initial build
