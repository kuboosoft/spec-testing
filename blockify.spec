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
Source1:    blockify-snapshot.sh
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

%clean
rm -rf %{buildroot}

%files 
%{_bindir}/blockify
%{_bindir}/blockify-dbus
%{_bindir}/blockify-ui
%{python2_sitelib}/blockify-%{version}-py2.7.egg-info/
%{python2_sitelib}/blockify/


%changelog

* Thu Jan 22 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.7.2-20150123-6865934-1
- Initial build rpm
