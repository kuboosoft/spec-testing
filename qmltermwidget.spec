#globals for qmltermwidget-0.1.0-20150126-4d93f02.tar
%global gitdate 20150126
%global gitversion 4d93f02
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}


Name:          qmltermwidget
Version:       0.1.0
Release:       1%{?gver}%{?dist}
Summary:       QML port of qtermwidget - development version

License:       GPLv2+
URL:           https://github.com/Swordfish90/qmltermwidget
Group:         System/X11/Terminals
Source:	       %{name}-%{version}-%{snapshot}.tar
Source1:       %{name}-snapshot.sh

BuildRequires:	git
BuildRequires: 	qt5-qtbase-devel 
BuildRequires:	qt5-qtdeclarative-devel
BuildRequires: 	qt5-qtquickcontrols	

%description
This project is a QML port of qtermwidget. It is written to be as close as 
possible to the upstream project in order to make cooperation possible.


%prep
%setup -q

%build
qmake-qt5
make %{?_smp_mflags}

%install

make INSTALL_ROOT=%{buildroot} install


%clean
rm -rf %{buildroot}

%files
%{_libdir}/qt5/qml/QMLTermWidget/


%changelog

* Mon Jan 26 2015 David Vasquez <davidjeremias82 at gmail dot com> - 0.1.0-20150126-4d93f02-1
- initial build rpm
