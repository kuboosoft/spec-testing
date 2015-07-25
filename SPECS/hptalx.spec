Name:hptalx
Version:1.3.1a
Release:1%{?dist}
Summary:is a program that allows us to connect the calculator HP to your PC 
Group:Applications/Engineering
License:GPLv2
URL:hptalx.sourceforge.net

BuildRequires:gtk2-devel >= 2.4
BuildRequires:glib2-devel >= 2.4
BuildRequires:libxml-devel >= 2.5
BuildRequires:ckermit >= 0.8
Requires:uucp

Source0:http://downloads.sourceforge.net/project/hptalx/hptalx/1.3.1a/hptalx-1.3.1a.tar.gz
Source1:%{name}.png

%description
This is HPTalx, a HP Calculator<->PC communications program for Linux, 
initially written by Bruno Barberi Gnecco, extended by Rafael Ostertag 
and allows you to backup and restore the memory of the calculator. 

Supports the connection of calculators HP 48, HP 48g +, HP 49g and HP 50g.

%prep
%setup -q n %{name}%{version}

%build
%configure 
make

%install
make install DESTDIR=%{buildroot}


# icons
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/

# menu
%__install -dm 755 %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Exec=hptalx
Icon=/usr/share/pixmaps/%{name}.png
Terminal=false
Name=hptalx
Comment=%{summary}
Categories=Utility;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(755, root, root)
%{_bindir}/hptalx
%{_docdir}/hptalx/hp49gplus.html
%{_docdir}/hptalx/hptalx.html
%{_mandir}/man1/hptalx.1.gz
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%post
connection.sh
#! /bin/bash
#Añadimos el modulo al kernel
cd /dev
modprobe hp4x
#Creamos una regla udev y agregamos nuestro usuario al grupo uucp
grupo=$(getent group | grep uucp); echo grupo=$grupo
usuario=$(loginctl show-session $XDG_SESSION_ID | cut -d= -f2 | tail -n 1); echo usuario=$usuario
current=$( echo $grupo | grep -o $usuario); echo "current=$current"
if [ "$usuario" == "$current" ]; then
echo "El usuario ya pertenece al grupo, sos un capo"
else
echo "dejate de joder que te voy a agregar"
fi﻿

%changelog
* Wed Jan 15 2014 Ronald Forero <L337.ronald AT gmail DOT com> -  1.3.1a-1
- Initial build rpm