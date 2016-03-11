#globals for libcec-3.0.1-20150725-3a41957.tar.xz
%global gitdate 20150725
%global gitversion 3a41957
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Name:          libcec
Version:       3.0.1
Release:       2%{?gver}%{dist}
Summary:       Library and utilities for HDMI-CEC device control

Group:         System Environment/Libraries
License:       GPLv2+
URL:           http://libcec.pulse-eight.com/
Source0:       %{name}-%{version}-%{snapshot}.tar.xz
Source1:       %{name}-snapshot.sh

BuildRequires: systemd-devel lockdev-devel
BuildRequires: git 
BuildRequires: cmake 
BuildRequires: platform-devel

%description
libCEC allows you in combination with the right hardware to control your device 
with your TV remote control over your existing HDMI cabling.

libCEC is an enabling platform for the CEC bus in HDMI, it allows developers to 
interact with other HDMI devices without having to worry about the communication 
overhead, handshaking, and the various ways of send messages for each vendor.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -n libcec

# Remove non linux binaries
rm support/p8-usbcec-driver-installer.exe
rm -rf driver

%build

%cmake .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS ChangeLog
%{_bindir}/cec-client
%{_bindir}/cec-client-3.0.1
%{_bindir}/cecc-client
%{_bindir}/cecc-client-3.0.1
%{_libdir}/libcec.so.*

%files devel
%{_includedir}/libcec
%{_libdir}/pkgconfig/libcec.pc
%{_libdir}/libcec.so

%changelog

* Mon Mar 07 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 3.0.1-20150725-3a41957-2
- Rebuilt for new release platform

* Fri Jul 24 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 3.0.1-20150725-3a41957-1
- Updated to 3.0.1-20150725-3a41957
- Added git tag in libcec-snapshot.sh

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.2.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Nov 10 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2.0-1
- Update to 2.2.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.4-1
- Update to 2.1.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.3-1
- Update to 2.1.3

* Mon Mar  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.0-1
- Update to 2.1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.5-1
- Update to 2.0.5

* Sun Nov 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.4-1
- Update to 2.0.4

* Mon Nov 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.3-1
- Update to 2.0.3

* Sun Nov  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.0-2
- Updates from review

* Wed Sep 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.0-1
- Update to 1.9.0

* Sat Jun 30 2012 Peter Robinson <pbrobinson@gmail.com> 1.7.1-1
- Initial packaging
