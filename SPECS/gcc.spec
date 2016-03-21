%global _islver 0.16.1
%global _cloogver 0.18.4
%global _mpfrver 3.1.4
%global _gmpver 6.1.0
%global _mpcver 1.0.3
%global gcc_target_platform %{_arch}-fedora-linux-gnu
%define debug_package %{nil}

Summary: Various compilers (C, C++, Objective-C, Java, ada, go, obj-c++ ...)
Name: gcc49
Version: 4.9.3
Release: 1%{?dist}

License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages

Source:  ftp://gcc.gnu.org/pub/gcc/releases/gcc-4.9.3/gcc-4.9.3.tar.bz2
Source1: http://isl.gforge.inria.fr/isl-%{_islver}.tar.bz2
Source2: http://www.bastoul.net/cloog/pages/download/cloog-%{_cloogver}.tar.gz
Source3: http://www.mpfr.org/mpfr-current/mpfr-%{_mpfrver}.tar.bz2
Source4: https://gmplib.org/download/gmp/gmp-%{_gmpver}.tar.bz2
Source5: ftp://ftp.gnu.org/gnu/mpc/mpc-%{_mpcver}.tar.gz
Patch:  target.path

# Patch1 for libitm: Don't redefine __always_inline in local_atomic.
# https://gcc.gnu.org/viewcvs/gcc?view=revision&revision=227040
Patch1: local_atomic.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: binutils >= 2.24
BuildRequires: make autoconf m4 gettext dejagnu bison flex sharutils
BuildRequires: texinfo texinfo-tex
BuildRequires: python-sphinx
BuildRequires: zlib-devel
BuildRequires: texinfo
BuildRequires: glibc-devel
#ada
BuildRequires: dejagnu

# go
BuildRequires: hostname, procps

# java
# BuildRequires: which
# BuildRequires: dejagnu
# BuildRequires: libart_lgpl-devel
# BuildRequires: gtk2-devel

Requires: binutils >= 2.24
Conflicts: gdb < 5.1-2
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true



%description
The gcc package contains the GNU Compiler Collection version 4.9.
You'll need this package in order to compile C code.



%prep
%setup -n gcc-4.9.3
%patch -p0
%patch1 -p0

tar jxvf %{SOURCE1} -C %{_builddir}/gcc-4.9.3/
tar zxvf %{SOURCE2} -C %{_builddir}/gcc-4.9.3/
tar jxvf %{SOURCE3} -C %{_builddir}/gcc-4.9.3/
tar jxvf %{SOURCE4} -C %{_builddir}/gcc-4.9.3/
tar zxvf %{SOURCE5} -C %{_builddir}/gcc-4.9.3/

  # link isl/cloog for in-tree builds
  ln -s isl-%{_islver} isl
  ln -s cloog-%{_cloogver} cloog
  ln -s mpfr-%{_mpfrver} mpfr
  ln -s gmp-%{_gmpver} gmp
  ln -s mpc-%{_mpcver} mpc

  # Do not run fixincludes
  sed -i 's@\./fixinc\.sh@-c true@' gcc/Makefile.in

  # Fedora Linux installs x86_64 libraries /lib

[[ $CARCH == "x86_64" ]] && sed -i '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64

  echo %{version} > gcc/BASE-VER

  # hack! - some configure tests for header files using "$CPP $CPPFLAGS"
  sed -i "/ac_cpp=/s/\$CPPFLAGS/\$CPPFLAGS -O2/" {libiberty,gcc}/configure

  mkdir -p %{_builddir}/gcc-build

%build
cd %{_builddir}/gcc-build
  # using -pipe causes spurious test-suite failures
  # http://gcc.gnu.org/bugzilla/show_bug.cgi?id=48565
  CFLAGS=${CFLAGS/-pipe/}
  CXXFLAGS=${CXXFLAGS/-pipe/}


  %{_builddir}/gcc-4.9.3/configure --prefix=/usr \
      --libdir=/usr/lib --libexecdir=%{_libexecdir} \
      --mandir=/usr/share/man --infodir=/usr/share/info \
      --enable-languages=c,c++,objc,obj-c++,go,fortran \
      --with-system-zlib \
      --with-linker-hash-style=gnu \
      --enable-libstdcxx-time \
      --disable-multilib \
      --program-suffix=-%{version} --enable-version-specific-runtime-libs \
      --enable-plugin \
      --enable-threads=posix \
      --enable-checking=release \
      --enable-gnu-unique-object \
      --enable-linker-build-id \
      --enable-initfini-array \
      --enable-gnu-indirect-function \
      --enable-tls \
      %ifarch %{ix86} x86_64
	  --with-tune=generic \
%endif
      --enable-bootstrap 
 

make bootstrap || return 1

  

%install

cd %{_builddir}/gcc-build

  make -j1 DESTDIR=%{buildroot} install

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{version}

  ## Lazy way of dealing with conflicting man and info pages and locales...
  rm -rf %{buildroot}/usr/share/
  rm -rf %{buildroot}/usr/include/
  find %{buildroot}/ -name \*iberty\* | xargs rm

  ## Delete debug
  rm -rf %{buildroot}/usr/src/debug/

  ## Delete redundant binaries
  rm -f %{buildroot}%{_bindir}/%{gcc_target_platform}*
  
  # Move potentially conflicting stuff to version specific subdirectory
  $(ls %{buildroot}/usr/lib/gcc/%{gcc_target_platform}/lib* &> /dev/null) && mv %{buildroot}/usr/lib/gcc/%{gcc_target_platform}/lib* %{buildroot}/usr/lib/gcc/%{gcc_target_platform}/%{version}/
  
  # Install Runtime Library Exception
  install -dm 755 %{buildroot}/usr/share/licenses/%{name}/
  install -m 0644 %{_builddir}/gcc-4.9.3/COPYING.RUNTIME %{buildroot}/usr/share/licenses/%{name}/RUNTIME.LIBRARY.EXCEPTION

  # Help plugins find out nvra.
  echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

 # Some packages expect the C preprocessor to be installed in the /lib directory. To support those packages, create this symlink:
  install -dm 755 %{buildroot}/lib/
  ln -svf %{_bindir}/cpp-%{version} %{buildroot}/lib/cpp-%{version}

 # Many packages use the name cc to call the C compiler. To satisfy those packages, create a symlink:

  ln -svf %{_bindir}/gcc-%{version} %{buildroot}/usr/bin/cc-%{version}

 # Add a compatibility symlink to enable building programs with Link Time Optimization (LTO):

  install -v -dm755 %{buildroot}/usr/lib/bfd-plugins
  ln -sfv %{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/liblto_plugin.so \
        %{buildroot}/usr/lib/bfd-plugins/


%files 

%{_bindir}/c++-4.9.3
%{_bindir}/cpp-4.9.3
%{_bindir}/g++-4.9.3
%{_bindir}/gcc-4.9.3
%{_bindir}/gcc-ar-4.9.3
%{_bindir}/gccgo-4.9.3
%{_bindir}/gcc-nm-4.9.3
%{_bindir}/gcc-ranlib-4.9.3
%{_bindir}/gcov-4.9.3
%{_bindir}/gfortran-4.9.3
%{_bindir}/cc-%{version}


%{_libexecdir}/gcc/%{gcc_target_platform}/4.9.3/
%{_datadir}/licenses/%{name}/RUNTIME.LIBRARY.EXCEPTION
%{_libdir}/go/4.9.3/%{gcc_target_platform}/
/usr/lib/gcc/%{gcc_target_platform}/4.9.3/
/usr/lib/bfd-plugins/
/lib/cpp-%{version}



%changelog
* Sat Oct 10 2015 David Vasquez <davidjeremias82@gmail.com> 4.9.3-1
- New package
