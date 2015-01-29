AutoReqProv: no

%define deb_opera %{name}-stable_%{version}_amd64.deb
%define deb_openssl libssl1.0.0_1.0.1f-1ubuntu2.8_amd64.deb

Summary: Opera Stable
Name: opera
Version: 27.0.1689.54
Release: 1%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://get.geo.opera.com/pub/opera-developer/
Source0: http://deb.opera.com/opera/pool/non-free/o/%{name}-stable/%{deb_opera}
Source1: http://mirrors.kernel.org/ubuntu/pool/main/o/openssl/%{deb_openssl}
Source2: opera-snapshot.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: x86_64
Requires: systemd-libs
Requires: libudev0
Requires: gtk2
Requires: desktop-file-utils
Requires: shared-mime-info
Requires: libXtst
Requires: GConf2
Requires: curl
Requires: libXScrnSaver
Requires: glibc
Requires: alsa-lib
Requires: nss
Requires: freetype
BuildRequires: binutils xz tar systemd-libs wget curl
# Provides: libcrypto.so.1.0.0()(64bit)
Obsoletes: opera-stable
Conflicts: opera-beta opera-next opera-developer

%description
Opera Stable

%prep

%setup -T -n %{name} -c

%build
ar p $RPM_SOURCE_DIR/%{deb_openssl} data.tar.xz | xz -d -9 | tar x -C $RPM_BUILD_DIR

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

# extract data from the deb package
ar p $RPM_SOURCE_DIR/%{deb_opera} data.tar.xz | xz -d -9 | tar x -C $RPM_BUILD_ROOT

# rename libdir
mv $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu/%{name} $RPM_BUILD_ROOT/usr/lib/
rm -rf $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}

# create new symlink
rm -f $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -sr $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

# delete some directories that is not needed on Fedora
rm -rf $RPM_BUILD_ROOT%{_datadir}/{lintian,menu}

# correct opera_sandbox permission
# FATAL:setuid_sandbox_client.cc(283)] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /usr/lib64/opera-developer/opera_sandbox is owned by root and has mode 4755.
chmod 4755 $RPM_BUILD_ROOT%{_libdir}/%{name}/opera_sandbox

# install libssl/libcrypto library
[ ! -d $RPM_BUILD_ROOT%{_libdir}/%{name}/lib ] && mkdir $RPM_BUILD_ROOT%{_libdir}/%{name}/lib
for i in libcrypto libssl; do
	cp -p $RPM_BUILD_DIR/lib/x86_64-linux-gnu/$i.so.* $RPM_BUILD_ROOT%{_libdir}/%{name}/lib
done

#find ./ -type f -exec sed -i 's:libudev.so.0:libudev.so.1:g' {} \;

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}

%changelog

* Wed Jan 28 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 27.0.1689.54-1
- Updated to 27.0.1689.54

* Sat Jan 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 26.0.1656.60-1
- Upstream
- Updated to 26.0.1656.60
- replaced libudev.so.0 symlink for libudev0
- Added snapshot, it will download the current Opera deb version.

* Wed Oct 22 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1655.0-2
- delete post and postun section
- install libudev.so.0 symlink in install section

* Wed Oct 22 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1655.0-1
- version up

* Sat Sep 27 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1632.0
- version up
- fix missing library requires
- fix missing symlink to opera-developer

* Sat Aug 30 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 25.0.1597.0
- version up

* Mon Jul 21 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1558.3
- version up

* Mon Jun 30 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1543.0
- version up
- change libssl/libcrypto install dir
- add package requires

* Thu Jun 26 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1537.0
- initial build
