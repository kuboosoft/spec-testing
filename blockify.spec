#globals for blockify-1.7.2-20150119-6865934.tar
%global gitdate 20150123
%global gitversion 6865934
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Name:       blockify
Summary:    Mutes Spotify advertisements
Version:    1.7.2
Release:    1%{?gver}%{?dist}
License:    MIT
Source0:    %{name}-%{version}-%{snapshot}.tar
Source1:    %{name}-snapshot.sh
Source2:    %{name}.png
Group:      Applications/Multimedia
BuildArch:  noarch
Url:        https://github.com/mikar/blockify

BuildRequires: pygtk2-devel python-devel python-setuptools gnome-python2-libwnck python-dbus alsa-utils gstreamer-python pulseaudio python-docopt
#-------------------------------------
Requires:   pygtk2 gnome-python2-libwnck python-dbus alsa-utils gstreamer-python pulseaudio python-docopt 


%description
Blockify is a linux only application that allows you to automatically mute 
songs and advertisements in Spotify. 

%prep
%setup -q 

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

# icon
install -dm 755 %{buildroot}/%{_datadir}/pixmaps
install -m 644 %{SOURCE2} %{buildroot}/%{_datadir}/pixmaps

# menu-entry
install -dm 755 %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=blockify
GenericName=blockify
Comment=Mutes Spotify advertisements
Icon=/usr/share/pixmaps/blockify.png
Type=Application
Categories=AudioVideo;
Exec=/usr/bin/blockify-ui
StartupNotify=false
Terminal=false
EOF

%clean
rm -rf %{buildroot}

%files 
%{_bindir}/blockify
%{_bindir}/blockify-dbus
%{_bindir}/blockify-ui
%{python2_sitelib}/blockify-%{version}-py2.7.egg-info/
%{python2_sitelib}/blockify/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/blockify.png


%changelog

* Thu Jan 22 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.7.2-20150123-6865934-1
- Initial build rpm
