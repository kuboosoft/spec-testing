#%define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod


Name:               rtlwifi-firmware-akmod
Version:            1
Release:     	    1%{?dist}
Summary:            rtlwifi kernel modules
Source0:            rtlwifi-firmware-akmod-1-20150911-2201a1d.tar
Source1:	    %{name}-snapshot.sh	
URL:                https://github.com/lwfinger/rtlwifi_new
Group:              System Environment/Kernel
License:	    Freeware
BuildRoot:          %{_tmppath}/build-%{name}-%{version}
BuildRequires:      %{_bindir}/kmodtool

ExclusiveArch:      i686 x86_64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the rtlwifi wireless firmware files
rtl8192ce, rtl8192se, rtl8192de, rtl8188ee, rtl8192ee, rtl8723ae, rtl8723be, and rtl8821ae.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

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
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done



%install
rm -rf ${RPM_BUILD_ROOT}


for kernel_version in %{?kernel_versions}; do
#    make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl_pci.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl_pci.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl_usb.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl_usb.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtlwifi.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtlwifi.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/btcoexist/btcoexist.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/btcoexist.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8188ee/rtl8188ee.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8188ee.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192c/rtl8192c-common.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192c-common.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192ce/rtl8192ce.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192ce.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192cu/rtl8192cu.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192cu.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192de/rtl8192de.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192de.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192ee/rtl8192ee.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192ee.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8192se/rtl8192se.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8192se.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8723ae/rtl8723ae.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8723ae.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8723be/rtl8723be.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8723be.ko
install -D -m 755 _kmod_build_${kernel_version%%___*}/rtl8821ae/rtl8821ae.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/rtl8821ae.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Sep 12 2015 David Vasquez <davidjeremias82 at gmail dot com> - 1-1
- Initial build
