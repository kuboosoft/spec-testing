#globals for platform-2.0.1-20160305-b31c75a.tar.xz
%global gitdate 20160305
%global gitversion b31c75a
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Name:           platform
Version:        2.0.1
Release:    	1%{?gver}%{dist}
Summary:        Platform support library used by libCEC and binary add-ons for Kodi

Group:          Applications/Multimedia

License:        GPLv3 and GPLv2+ and LGPLv2+ and MIT
URL:            https://github.com/Pulse-Eight/platform
Source:		%{name}-%{version}-%{snapshot}.tar.xz
Source1:	%{name}-snapshot.sh

BuildRequires:	cmake
BuildRequires:	git


%description
Platform support library used by libCEC and binary add-ons for Kodi .

%package devel
Summary:        platform devel files
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for platform


%prep
%setup -n  platform


%build
cmake . \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=1 \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_LIBDIR_NOARCH=%{_libdir}

make 
 

%install
make install DESTDIR=%{buildroot}



%files 
%{_includedir}/platform/os.h
%{_includedir}/platform/posix/os-socket.h
%{_includedir}/platform/posix/os-threads.h
%{_includedir}/platform/posix/os-types.h
%{_includedir}/platform/sockets/cdevsocket.h
%{_includedir}/platform/sockets/socket.h
%{_includedir}/platform/sockets/tcp.h
%{_includedir}/platform/threads/atomics.h
%{_includedir}/platform/threads/mutex.h
%{_includedir}/platform/threads/threads.h
%{_includedir}/platform/util/StdString.h
%{_includedir}/platform/util/StringUtils.h
%{_includedir}/platform/util/atomic.h
%{_includedir}/platform/util/buffer.h
%{_includedir}/platform/util/timeutils.h
%{_includedir}/platform/util/util.h
%{_libdir}/libplatform.so
%{_libdir}/libplatform.so.*

%files devel
%{_libdir}/pkgconfig/platform.pc
%{_libdir}/platform/platform-config.cmake

%changelog

* Sat Mar 05 2016 David Vásquez <davidjeremias82 at gmail dot com> - 2.0.1-20160305-b31c75a-1
- Updated to 2.0.1-20160305-b31c75a

* Wed Jul 29 2015 David Vasquez <davidjeremias82 at gmail dot com> - 1.0.10-20150729-278828a-1
- Updated to 1.0.10-20150729-278828a

* Wed May 20 2015 David Vasquez <davidjeremias82 at gmail dot com> - 1.0.9-20150520-aafa6e9-1
- Initial build rpm
