#globals for kvantum-0.8.9-20150124-658f8f6.tar
%global gitdate 20150124
%global gitversion 658f8f6
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}


%global	realname Kvantum

Name:          kvantum
Version:       0.8.9
Release:       1%{?dist}
Summary:       SVG-based theme engine for Qt4/Qt5 and KD

License:       GPLv2+
URL:           https://github.com/tsujan/Kvantum
Group:         Development/Libraries
Source:	       %{name}-%{version}-%{snapshot}.tar
Source1:       %{name}-snapshot.sh

BuildRequires:	git
BuildRequires: 	qt5-qtbase-devel 
BuildRequires:	qt5-qtx11extras-devel
BuildRequires:	qt5-qtsvg-devel	

%description
A Linux SVG-based theme engine for Qt4/Qt5 and KDE


%prep
%setup -q

%build

for _fronted in kvantummanager kvantumpreview style; do
    cd $_fronted
    qmake-qt5
    make
    cd ..
  done

qmake-qt5
make

%install

install -dm 755 %{buildroot}/%{_datadir}/doc/%{name}
install -dm 755 %{buildroot}/%{_bindir}

install -Dm0644 ./style/libkvantum.so %{buildroot}/%{_libdir}/qt5/plugins/styles/libkvantum.so
install -Dm0644 ./color/%{realname}.colors %{buildroot}/%{_datadir}/apps/color-schemes/%{realname}.colors

install -dm 755 %{buildroot}/%{_libdir}/qt4/plugins/styles
ln -sf %{_libdir}/qt5/plugins/styles/libkvantum.so %{buildroot}/%{_libdir}/qt4/plugins/styles/libkvantum.so

install -m 0644 ./kvantummanager/kvantummanager  %{buildroot}/%{_bindir}/
install -m 0644 ./kvantumpreview/kvantumpreview  %{buildroot}/%{_bindir}/
chmod a+x %{buildroot}/%{_bindir}/kvantummanager
chmod a+x %{buildroot}/%{_bindir}/kvantumpreview

cp -rf ./doc/* %{buildroot}/%{_datadir}/doc/%{name}/
install -Dm0644 ./kvantumpreview/kvantum.svg %{buildroot}/%{_datadir}/pixmaps/kvantum.svg
install -Dm0644 ./kvantummanager/data/kvantummanager.desktop %{buildroot}/%{_datadir}/applications/kvantummanager.desktop

%clean
rm -rf %{buildroot}

%files
%{_bindir}/kvantumpreview
%{_bindir}/kvantummanager
%{_datadir}/apps/color-schemes/%{realname}.colors
%{_datadir}/applications/kvantummanager.desktop
%{_datadir}/doc/%{name}/
%{_datadir}/usr/share/pixmaps/kvantum.svg
%{_libdir}/qt5/plugins/styles/libkvantum.so
%{_libdir}/qt4/plugins/styles/libkvantum.so

%changelog

* Sat Jan 24 2015 David Vasquez <davidjeremias82 at gmail dot com> - 0.8.9-20150124-658f8f6-1
- initial build rpm
