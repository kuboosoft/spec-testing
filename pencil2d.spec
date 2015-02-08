#globals for pencil2d-0.5.4-20150207-2630deb.tar
%global gitdate 20150207
%global gitversion 2630deb
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}


Name:          pencil2d
Version:       0.5.4
Release:       1%{?gver}%{?dist}
Summary:       Animation/drawing software.

License:       GPLv2+
URL:           http://www.pencil2d.org/
Group:         Development/Libraries
Source:	       %{name}-%{version}-%{snapshot}.tar
Source1:       %{name}-snapshot.sh

BuildRequires:	git
BuildRequires: 	qt5-qtbase-devel 
BuildRequires:	qt5-qtmultimedia-devel
BuildRequires:	qt5-qtsvg-devel	
BuildRequires:	ming-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qt5-qtxmlpatterns-devel
BuildRequires:	qt5-qttools-devel
BuildRequires:	zlib-devel
#BuildRequires:	quazip-devel

Requires:	hicolor-icon-theme 
Requires:	qt5-qtmultimedia 
Requires:	qt5-qtxmlpatterns 
Requires:	zlib 
#Requires:	quazip	

%description
Pencil2D is an animation/drawing software for Mac OS X, Windows, and Linux. 
It lets you create traditional hand-drawn animation (cartoon) using both bitmap 
and vector graphics.


%prep
%setup -q

%build

qmake-qt5
make

%install


install -D -m755 app/Pencil2D %{buildroot}/usr/bin/pencil2d
install -D -m644 icons/icon.png %{buildroot}/%{_datadir}/pixmaps/pencil2d.png


# menu-entry
install -dm 755 %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Name=Pencil
Exec=pencil2d %F
Icon=/usr/share/pixmaps/pencil2d.png
Categories=Graphics;2DGraphics;
EOF

%files
%{_bindir}/pencil2d
%{_datadir}/pixmaps/pencil2d.png
%{_datadir}/applications/pencil2d.desktop

%changelog

* Sat Feb 07 2015 David Vasquez <davidjeremias82 at gmail dot com> - 0.8.9-20150207-2630deb-1
- initial build rpm
