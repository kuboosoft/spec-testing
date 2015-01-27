#globals for cool-retro-term-1.0.0-20150126-edad3ab.tar
%global gitdate 20150126
%global gitversion edad3ab
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}


Name:          cool-retro-term
Version:       1.0.0
Release:       1%{?gver}%{?dist}
Summary:       Cool Retro Terminal

License:       GPLv2+
URL:           https://github.com/tsujan/cool-retro-term
Group:         System/X11/Terminals
Source:	       %{name}-%{version}-%{snapshot}.tar
Source1:       %{name}-snapshot.sh

BuildRequires:	git
BuildRequires: 	qt5-qtbase-devel 
BuildRequires: 	qt5-qtquickcontrols
BuildRequires:	qt5-qtgraphicaleffects
BuildRequires:	desktop-file-utils
BuildRequires:	qt5-qtdeclarative-devel	

Requires:	qt5-qtdeclarative
Requires:	qt5-qtgraphicaleffects
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtbase

%description
cool-retro-term is a terminal emulator which mimics the look and feel of the 
old cathode tube screens. It has been designed to be eye-candy, customizable, 
and reasonably lightweight.


%prep
%setup -q
sed -i '/qmltermwidget/d' cool-retro-term.pro

%build
qmake-qt5
make %{?_smp_mflags}

%install

make INSTALL_ROOT=%{buildroot} install

desktop-file-install                            \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
%{name}.desktop

%clean
rm -rf %{buildroot}

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*

%changelog

* Mon Jan 26 2015 David Vasquez <davidjeremias82 at gmail dot com> - 1.0.0-20150126-edad3ab-1
- initial build rpm
