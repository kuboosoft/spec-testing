%global realname ExMplayer
%global _with_ffmpeg 0
%global _with_ffmpegex 1


Name:          exmplayer
Version:       5.0.1
Release:       1%{?dist}
Summary:       MPlayer GUI with thumbnail seeking, 3D Video support,

License:       GPLv2+
URL:           http://%{name}.sourceforge.net/
Group:         Applications/Multimedia
Source:	       https://launchpad.net/~%{name}-dev/+archive/%{name}/+files/%{name}_%{version}.tar.gz

BuildRequires: 	qt-devel 

Requires:	mplayer	
Requires:	ffmpeg

%description
ExMplayer (Extended MPlayer) is a GUI front-end for MPlayer with flow view 
and tool like media cutter.It can play audio,video,dvd files(.vob),vcd 
iles(.mpg,.dat) etc and supports network streaming.It supports subtitles,
subtitle decoding is done by using ass library.It can play any media formats
without any external codecs.


%prep
%setup -n %{realname}

%build
cd ./src
qmake-qt4
make

%install

install -Dm755 src/%{name} %{buildroot}/usr/bin/%{name}
#
install -dm755 %{buildroot}/usr/share/applications
install -m644 %{name}.desktop %{name}_enqueue.desktop %{buildroot}/usr/share/applications
install -Dm644 debian/%{name}.png %{buildroot}/usr/share/pixmaps/%{name}.png
#
install -dm755 %{buildroot}/etc/%{name}
install -m644 linux_build/{sc_default.xml,fmts} %{buildroot}/etc/%{name}
#
install -dm755 %{buildroot}/usr/share/%{name}

%if 0%{?_with_ffmpegex}
# use native installed ffmpeg 
ln -sf /usr/bin/ffmpeg  %{buildroot}/usr/share/%{name}/ffmpeg
%endif

%if 0%{?_with_ffmpeg}
install -m755 linux_build/ffmpeg %{buildroot}/usr/share/%{name}
%endif


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}_enqueue.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/
%{_sysconfdir}/%{name}/fmts
%{_sysconfdir}/%{name}/sc_default.xml
%{_datadir}/%{name}/ffmpeg


%changelog

* Sat Aug 22 2015 David Vasquez <davidjeremias82 at gmail dot com> - 5.0.1-1
- Updated to 5.0.1

* Tue Jul 28 2015 Rupesh Sreeraman <exmplayer.dev@gmail.com> - 5.0.0-1
- updated  for version 5

* Sat Apr 04 2015 David Vasquez <davidjeremias82 at gmail dot com> - 3.8.0-2
- Excluded ffmpeg-devel

* Sat Feb 07 2015 David Vasquez <davidjeremias82 at gmail dot com> - 3.8.0-1
- initial build rpm
