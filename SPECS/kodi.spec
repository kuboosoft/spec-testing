%bcond_with nonfree 

#globals for kodi-16.0-20160303-a5f3a99.tar.xz
%global gitdate 20160303
%global gitversion a5f3a99
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

%define _libtag_ver %(version="`rpm -q --qf '%{VERSION}' taglib-devel`"; echo "$version")

Name:        kodi
Version:     16.0
Release:     2%{?gver}%{dist}
Summary:     Kodi Media center
License:     GPLv2+ and GPLv3+ and LGPLv2+ and BSD and MIT
Group:       Productivity/Multimedia/Video/Players
Url:         http://kodi.tv/

# Source 0: with kodi-snapshot.sh, includes git submodules
# also contains code called "redundant private" but if you remove it, you can affect the performance; 
# and external components as kodi-pvr-addons. 
# The best choice is not remove it; an minor increased of space; isn't death. 

Source0:     %{name}-%{version}-%{snapshot}.tar.xz
Source1:     %{name}-snapshot.sh
#-------------------------------------
# PATCH no make symbolic links
Patch:      no-xbmc-symbolic-link.patch
#-------------------------------------
BuildRoot:   %{_tmppath}/%{name}-%{version}-build
ExcludeArch: ppc64

Obsoletes:   xbmc <= %{version}
Provides:    xbmc = %{version}


%if 0%{?fedora} >= 14
BuildRequires:  gettext-autopoint
%else
BuildRequires:  gettext
%endif

BuildRequires:  trousers-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXt-devel
BuildRequires:  bzip2-devel
#BuildRequires: libX11-devel
BuildRequires:  glew-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libcec-devel >= 3.0.0
BuildRequires:  redhat-lsb
BuildRequires:  afpfs-ng-devel
BuildRequires:  yajl-devel
BuildRequires:  nettle-devel
BuildRequires:  hdhomerun-devel
BuildRequires:  gnutls-devel
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL_image)
BuildRequires:  pkgconfig(SDL_mixer)
BuildRequires:  expat-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bluez-libs-devel
BuildRequires:  freetype-devel
BuildRequires:  avahi-devel
BuildRequires:  boost-devel
BuildRequires:  ccache
# needed to delete the fixed rpath introduced by smbclient
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  curl curl-devel
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  enca-devel
BuildRequires:  fdupes
BuildRequires:  flac-devel
BuildRequires:  flex
BuildRequires:  fontconfig-devel
BuildRequires:  fribidi-devel
BuildRequires:  ftgl-devel
BuildRequires:  gcc-c++
%ifnarch %{arm}
BuildRequires:  glew-devel
%endif
BuildRequires:  glibc-devel
BuildRequires:	gmp-devel
BuildRequires:  gperf
BuildRequires:  java
BuildRequires:  libass-devel >= 0.9.7
BuildRequires:  libbluray-devel
BuildRequires:  libcdio-devel
%ifarch %ix86 x86_64
BuildRequires:  libcrystalhd-devel
%endif
BuildRequires:  libdvdread-devel
%if %{with nonfree}
BuildRequires:  libmad-devel
BuildRequires:  faac-devel 
BuildRequires:  libmpeg2-devel 
BuildRequires:	dcadec-devel
BuildRequires:  librtmp-devel
%endif
# new
BuildRequires:	libuuid-devel
BuildRequires:	crossguid-devel
# new
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  libjasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libnfs-devel
BuildRequires:  libogg-devel
BuildRequires:  pcre-devel
BuildRequires:  libplist-devel
BuildRequires:  libpng-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  shairplay-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libssh-devel
BuildRequires:  libstdc++-devel
BuildRequires: 	taglib-devel
BuildRequires:  libtiff-devel
BuildRequires:  libtool
BuildRequires:  libudev-devel
BuildRequires:  libva-devel
%ifnarch %{arm}
BuildRequires:  libvdpau-devel
%endif
BuildRequires:  libvorbis-devel
BuildRequires:  lzo-devel
BuildRequires:  mysql-devel
BuildRequires:  nasm
BuildRequires:  pcre-devel
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  sqlite-devel
BuildRequires:  swig
BuildRequires:  tinyxml-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  unzip
BuildRequires:  libcap-devel
BuildRequires:  yasm
BuildRequires:  byacc
BuildRequires:  zip
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	git
%ifarch %{arm}
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
%endif

#Samba libwbclient
# BuildRequires:	libwbclient-compat
BuildRequires:	libwbclient

# for goom2k4
BuildRequires:	gtk2-devel glib-devel gtk+-devel xmms-devel

#-------------------------------------
## kodi needs the same libtag version which was used to build against
Requires:       taglib = %{_libtag_ver}
# kodi needs libnfs to access nfs sources, it is not automatically required
Requires:       libnfs
#
Requires: libbluray
Requires: libcec >= 3.0.0
Requires: libcrystalhd

# needed when doing a minimal install, see
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1844
Requires: glx-utils
Requires: xorg-x11-utils

# This is just symlinked to, but needed both at build-time
# and for installation
Requires: python-pillow
#-------------------------------------

# libwbclient compatibility
Requires: libwbclient

%description
KODI media center is a free cross-platform media-player jukebox and
entertainment hub.  KODI can play a spectrum of of multimedia formats,
and featuring playlist, audio visualizations, slideshow, and weather
forecast functions, together third-party plugins.

%package devel
Summary:        Kodi Media center devel files
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}-%{release}
Obsoletes: 	xbmc-devel < 14.0
Provides: 	xbmc-devel = %{version}


%description devel
Development files for the Kodi media Center


%prep
%setup -n xbmc

%patch -p0

chmod +x bootstrap

./bootstrap -prefix=/usr

export MAKE=make

%build

make -C tools/depends/native/JsonSchemaBuilder/

./configure \
--prefix=%{_prefix} --bindir=%{_bindir} --includedir=%{_includedir} \
--libdir=%{_libdir} --datadir=%{_datadir} \
--with-lirc-device=/var/run/lirc/lircd \
--disable-rsxs \
--enable-goom \
--enable-pulse \
--enable-joystick \
--enable-libcec \
--enable-ssh \
--disable-dvdcss \
--enable-libbluray \
--disable-optimizations --disable-debug \
%ifnarch %{arm}
--enable-gl \
--disable-gles \
--enable-vdpau \
%else
--enable-gles \
--disable-vdpau \
--disable-vaapi \
%ifarch armv7hl \
--enable-tegra \
--disable-neon \
%endif
%ifarch armv7hnl
--enable-neon \
%endif
%endif

make %{?_smp_mflags} VERBOSE=1

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
# remove the doc files from unversioned /usr/share/doc/kodi, they should be in versioned docdir
rm -r %{buildroot}/%{_datadir}/doc/

# copy manpages
install -m 644 -D docs/manpages/kodi-standalone.1 %{buildroot}%{_mandir}/man1/kodi-standalone.1
install -m 644 -D docs/manpages/kodi.bin.1 %{buildroot}%{_mandir}/man1/kodi.1

# remove win32 source files
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.addon/dlfcn-win32.cpp
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.addon/dlfcn-win32.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.addon/dlfcn-win32.cpp
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.addon/dlfcn-win32.h

# remove duplicate header files
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.addon/libXBMC_addon.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.addon/libXBMC_addon.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.codec/libXBMC_codec.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.codec/libXBMC_codec.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.gui/libXBMC_gui.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.gui/libXBMC_gui.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.kodi.pvr/libXBMC_pvr.h
rm -f %{buildroot}%{_kodi_addons_dir}/library.xbmc.pvr/libXBMC_pvr.h

desktop-file-install \
 --dir=%{buildroot}%{_datadir}/applications \
 %{buildroot}%{_datadir}/applications/kodi.desktop

# delete fixed rpath from smbclient.pc - this fixes
# http://trac.kodi.tv/ticket/15497 and
# http://bugzilla.opensuse.org/show_bug.cgi?id=902421
chrpath %{buildroot}%{_libdir}/kodi/kodi.bin >/dev/null 2>&1 && \
  chrpath -d %{buildroot}%{_libdir}/kodi/kodi.bin

%ifarch x86_64 
sed -i 's|/usr/lib/kodi|/usr/lib64/kodi|g' %{buildroot}/%{_libdir}/kodi/kodi-config.cmake
%endif

%fdupes %{buildroot}

%files
%defattr(-,root,root)
%doc copying.txt LICENSE.GPL docs/README.linux
%{_bindir}/kodi
%{_bindir}/xbmc
%{_bindir}/kodi-standalone
%{_bindir}/xbmc-standalone
%{_datadir}/xsessions/kodi.desktop
%{_datadir}/xsessions/xbmc.desktop
%{_datadir}/applications/kodi.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/kodi/
%{_mandir}/man1/kodi.1.gz
%{_mandir}/man1/kodi-standalone.1.gz
%{_libdir}/kodi/


%files devel
%defattr(-,root,root)
%{_includedir}/kodi/DVDDemuxPacket.h
%{_includedir}/kodi/libXBMC_addon.h
%{_includedir}/kodi/libXBMC_codec.h
%{_includedir}/kodi/libXBMC_pvr.h
%{_includedir}/kodi/xbmc_addon_cpp_dll.h
%{_includedir}/kodi/xbmc_addon_dll.h
%{_includedir}/kodi/xbmc_addon_types.h
%{_includedir}/kodi/xbmc_codec_types.h
%{_includedir}/kodi/xbmc_epg_types.h
%{_includedir}/kodi/xbmc_pvr_dll.h
%{_includedir}/kodi/xbmc_pvr_types.h
%{_includedir}/kodi/xbmc_scr_dll.h
%{_includedir}/kodi/xbmc_scr_types.h
%{_includedir}/kodi/xbmc_stream_utils.hpp
%{_includedir}/kodi/xbmc_vis_dll.h
%{_includedir}/kodi/xbmc_vis_types.h
%{_includedir}/kodi/xbmc_audioenc_dll.h
%{_includedir}/kodi/xbmc_audioenc_types.h

%{_includedir}/kodi/AEChannelData.h
%{_includedir}/kodi/kodi_audiodec_dll.h
%{_includedir}/kodi/kodi_audiodec_types.h
%{_includedir}/kodi/libKODI_guilib.h

%{_includedir}/kodi/kodi_adsp_dll.h
%{_includedir}/kodi/kodi_adsp_types.h
%{_includedir}/kodi/kodi_audioengine_types.h
%{_includedir}/kodi/libKODI_adsp.h
%{_includedir}/kodi/libKODI_audioengine.h



%changelog

* Thu Mar 03 2016 David Vásquez <davidjeremias82 at gmail dot com> - 16.0-20160303-a5f3a99-2
- Updated to 16.0-20160303-a5f3a99

* Mon Oct 19 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.2-20151019-02e7013-1
- Updated to 15.2-20151019-02e7013

* Thu Sep 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.1-20150910-f4dda26-1
- Updated to 15.1-20150910-f4dda26

* Wed Jul 29 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.0-20150724-2f34a0c-1
- Updated to 15.0-20150729-2f34a0c

* Wed May 20 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.0b1-20150520-d1a2c33-1
- Updated to 15.0b1-20150520-d1a2c33

* Mon May 18 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 14.2-20150518-7cc53a9-2
- Initial build
