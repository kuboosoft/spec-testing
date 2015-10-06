Name:		rtlwifi-firmware
Version:	1
Release:	1%{?dist}
Summary:	rtlwifi userland package

Group:		System Environment/Kernel
License:	Freeware
URL:		https://github.com/lwfinger/rtlwifi_new

Requires: %{name}-kmod  >= %{version}
Provides: %{name}-kmod-common = %{version}

ExclusiveArch:      i686 x86_64

%description 
userland package for more details http://rpmfusion.org/Packaging/KernelModules/Kmods2#userland_package

%files


%changelog
* Thu Sep 17 2015 Sérgio Basto <sergio@serjux.com> - 1-1
- Initial userland package

