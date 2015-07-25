%define debug_package %{nil}

%ifarch x86_64
%global	arc 64
%global	libpath	lib64
%global archdir x86_64
%else
%global	arc 32
%global	libpath	lib
%global archdir x86
%endif

%global	urlref http://support.amd.com/en-us/download/desktop?os=Linux+x86
%global	DLAGENTS http::/usr/bin/curl --referer %{urlref} -o %o %u
%global	amdname amd-catalyst-omega
%global	amdver 14.501.1003


Name:		catalyst-utils
Version:	14.12
Release:	1%{?dist}
Summary:	AMD/ATI drivers. Auto re-compile fglrx module while shutdown/reboot.
Group:		User Interface/X Hardware Support

License:	Redistributable, no modification permitted
URL:		http://www.amd.com

Source:		http://www2.ati.com/drivers/linux/%{amdname}-%{version}-linux-run-installers.zip
Source1:    	catalyst.sh
Source2:    	atieventsd.sh
Source3:    	atieventsd.service
Source4:    	catalyst.conf
Source6:    	switchlibGL
Source7:    	switchlibglx
Source8:    	pxp_switch_catalyst
Source9:    	temp_links_catalyst
Source10:    	temp-links-catalyst.service
Patch0:    	arch-fglrx-authatieventsd_new.patch

# catalyst hook
Source11:  hook-fglrx
Source12:  catalyst_build_module
Source13:  ati_make.sh
Patch1:    makefile_compat.patch
Source14:  catalyst-hook.service
Source15:  %{name}-snapshot.sh
Patch2:    lano1106_fglrx_intel_iommu.patch
Patch3:    lano1106_kcl_agp_13_4.patch
Patch4:    lano1106_fglrx-13.8_proc.patch
Patch5:    cold-fglrx-3.14-current_euid.patch
Patch6:    fglrx_gpl_symbol.patch
Patch7:    fglrx_3.17rc6-no_hotplug.patch

BuildRequires:	binutils libtool curl chrpath
#-------------------------------------
Requires:	xorg-x11-server-Xorg >= 1.7.0 
Requires:	xorg-x11-server-Xorg < 1.17.0 
Requires:	libXrandr 
Requires:	libSM 
Requires:	fontconfig 
Requires:	libXcursor 
Requires:	libXi 
Requires:	gcc 
Requires:	libXinerama
Requires:	libtool

# OPTIONAL
# to run ATi Catalyst Control Center (amdcccle)
Requires:	qt 
# to run ATi Catalyst Control Center (amdcccle)
Requires:	libXxf86vm 
# acpi event support  / atieventsd
Requires:	acpid 
# Catalyst drivers libraries symlinks.
Requires:	catalyst-libgl
# OpenCL implemention for AMD Catalyst 
Requires:	opencl-catalyst 
%ifarch x86_64
# Utilities and libraries (32-bit)
Requires: libXext(x86-32)
Requires: libdrm(x86-32) 
Requires: catalyst-utils 
Requires: libXinerama(x86-32)
%endif
#-------------------------------------
Conflicts:       xorg-x11-drv-nvidia
Conflicts:       xorg-x11-drv-nvidia-legacy
Conflicts:       xorg-x11-drv-nvidia-71xx
Conflicts:       xorg-x11-drv-nvidia-96xx
Conflicts:       xorg-x11-drv-nvidia-173xx
Conflicts:       xorg-x11-drv-nvidia-beta
Conflicts:       xorg-x11-drv-nvidia-newest
Conflicts:       xorg-x11-drv-nvidia-custom
Conflicts:       xorg-x11-drv-fglrx

# ATI auto-generated RPMs
Conflicts:       ATI-fglrx
Conflicts:       ATI-fglrx-control-panel
Conflicts:       ATI-fglrx-devel
Conflicts:       kernel-module-ATI-fglrx
Conflicts:       ATI-fglrx-IA32-libs

Conflicts:	catalyst-test catalyst-total catalyst-total-pxp catalyst-utils-pxp
Provides:	libatical=%{version} dri libtxc_dxtn


%description
AMD/ATI drivers. Utilities and libraries. Radeons HD 2 3 4 xxx ARE NOT SUPPORTED


%package -n catalyst-libgl
Requires:	catalyst-utils = %{version}-%{release} 
Requires:	mesa-filesystem >= 10.1.0-4
Conflicts:	mesa-libGL mesa-libEGL-devel
Provides:	mesa-libGL 
Summary:	Catalyst drivers libraries symlinks + experimental powerXpress support

%description -n catalyst-libgl
AMD/ATI drivers. Catalyst drivers libraries symlinks + experimental powerXpress support.


%package -n opencl-catalyst
#Provides:	libcl ocl-icd
Conflicts:	ocl-icd ocl-icd-devel
Requires:	gcc
# headers necessary for OpenCL development
Requires:	opencl-headers
Summary:	OpenCL implemention for AMD Catalyst

%description -n opencl-catalyst
AMD/ATI drivers. OpenCL implemention for AMD Catalyst


%package -n catalyst-hook
#Provides:	catalyst 
Conflicts:	catalyst-test catalyst-daemon catalyst catalyst-generator catalyst-dkms
Requires:	catalyst-utils = %{version}-%{release} 
Requires:	gcc >= 4.0.0 
Requires:	make 
Requires:	kernel-devel < 3.19 
Requires:	kernel-headers
# headers necessary for OpenCL development
Requires:	opencl-headers
Summary:	Auto re-compile fglrx module while shutdown/reboot

%description -n catalyst-hook
AMD/ATI drivers. Auto re-compile fglrx module while shutdown/reboot.


%prep
%setup -n fglrx-14.501.1003


%build
# cd fglrx-%{amdver}
sh amd-driver-installer-%{amdver}-x86.x86_64.run --extract archive_files

%install
# cd fglrx-%{amdver}
# catalyst-libgl

      install -m755 -d %{buildroot}/usr/lib/xorg/modules/extensions
      ln -snf /usr/lib/xorg/modules/extensions/fglrx/fglrx-libglx.so %{buildroot}/usr/lib/xorg/modules/extensions/libglx.so

      install -m755 -d %{buildroot}/usr/lib/fglrx
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/fglrx/libGL.so.1.2.0
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/fglrx/libGL.so.1
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/fglrx/libGL.so
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/libGL.so.1.2.0
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/libGL.so.1
      ln -snf /usr/lib/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/libGL.so


      # We have to provide symlinks to mesa, as catalyst doesn't ship them
      ln -s /usr/lib/mesa/libEGL.so.1.0.0 %{buildroot}/usr/lib/libEGL.so.1.0.0
      ln -s libEGL.so.1.0.0	          %{buildroot}/usr/lib/libEGL.so.1
      ln -s libEGL.so.1.0.0               %{buildroot}/usr/lib/libEGL.so

      ln -s /usr/lib/mesa/libGLESv1_CM.so.1.1.0 %{buildroot}/usr/lib/libGLESv1_CM.so.1.1.0
      ln -s libGLESv1_CM.so.1.1.0	        %{buildroot}/usr/lib/libGLESv1_CM.so.1
      ln -s libGLESv1_CM.so.1.1.0               %{buildroot}/usr/lib/libGLESv1_CM.so

      ln -s /usr/lib/mesa/libGLESv2.so.2.0.0 %{buildroot}/usr/lib/libGLESv2.so.2.0.0
      ln -s libGLESv2.so.2.0.0               %{buildroot}/usr/lib/libGLESv2.so.2
      ln -s libGLESv2.so.2.0.0               %{buildroot}/usr/lib/libGLESv2.so


     # powerXpress
      install -m755 %{SOURCE6} %{buildroot}/usr/lib/fglrx
      install -m755 %{SOURCE7} %{buildroot}/usr/lib/fglrx
      # switching script: switch xorg.conf + aticonfig --px-Xgpu + switchlibGL + add/remove fglrx into MODULES
      install -m755 -d %{buildroot}/usr/bin
      install -m755 %{SOURCE8} %{buildroot}/usr/bin
	
     # License
     #install -m755 -d %{buildroot}/usr/share/licenses
     #ln -s catalyst-utils %{buildroot}/usr/share/licenses/%{name}


# package opencl-catalyst
 
%ifarch x86_64
cd %{_builddir}/fglrx-%{amdver}/archive_files/arch/x86_64
%else
cd %{_builddir}/fglrx-%{amdver}/archive_files/arch/x86
%endif
      

      install -m755 -d %{buildroot}/etc/OpenCL/vendors
      install -m644 etc/OpenCL/vendors/amdocl%{arc}.icd %{buildroot}/etc/OpenCL/vendors

      install -m755 -d %{buildroot}/usr/lib
      cp -f ./usr/%{libpath}/libamdocl*.so %{buildroot}/usr/lib
      cp -f ./usr/%{libpath}/libOpenCL.so.1 %{buildroot}/usr/lib
      ln -sf /usr/lib/libOpenCL.so.1 %{buildroot}/usr/lib/libOpenCL.so

      install -m755 -d %{buildroot}/usr/bin
      install -m755 usr/bin/clinfo %{buildroot}/usr/bin

     # License
      # install -m755 -d %{buildroot}/usr/share/licenses
     # ln -s catalyst-utils %{buildroot}/usr/share/licenses/%{name}


# package catalyst-utils


  ## Install userspace tools and libraries
    # Create directories
      install -m755 -d %{buildroot}/etc/ati
      install -m755 -d %{buildroot}/etc/rc.d
      install -m755 -d %{buildroot}/etc/profile.d
      install -m755 -d %{buildroot}/etc/acpi/events
      install -m755 -d %{buildroot}/etc/security/console.apps

      install -m755 -d %{buildroot}/usr/lib/xorg/modules/dri
      install -m755 -d %{buildroot}/usr/lib/xorg/modules/drivers
      install -m755 -d %{buildroot}/usr/lib/xorg/modules/extensions/fglrx
      install -m755 -d %{buildroot}/usr/lib/xorg/modules/linux
      install -m755 -d %{buildroot}/usr/lib/dri
      install -m755 -d %{buildroot}/usr/lib/fglrx
      install -m755 -d %{buildroot}/usr/lib/systemd/system
#       install -m755 -d %{buildroot}/usr/lib/hsa

      install -m755 -d %{buildroot}/usr/bin

      install -m755 -d %{buildroot}/usr/include/GL

      install -m755 -d %{buildroot}/usr/share/applications
      install -m755 -d %{buildroot}/usr/share/ati/amdcccle
      install -m755 -d %{buildroot}/usr/share/licenses/%{name}
      install -m755 -d %{buildroot}/usr/share/man/man8
      install -m755 -d %{buildroot}/usr/share/pixmaps

    # X.org driver
%ifarch x86_64
cd %{_builddir}/fglrx-%{amdver}/archive_files/xpic_64a/usr/X11R6/lib64/modules
%else
cd %{_builddir}/fglrx-%{amdver}/archive_files/xpic/usr/X11R6/lib/modules
%endif

      install -m755 *.so %{buildroot}/usr/lib/xorg/modules
      install -m755 drivers/*.so %{buildroot}/usr/lib/xorg/modules/drivers
      install -m755 linux/*.so %{buildroot}/usr/lib/xorg/modules/linux
      install -m755 extensions/fglrx/fglrx-libglx.so %{buildroot}/usr/lib/xorg/modules/extensions/fglrx/fglrx-libglx.so

    # Controlcenter / libraries

%ifarch x86_64
cd %{_builddir}/fglrx-%{amdver}/archive_files/arch/x86_64/usr
%else
cd %{_builddir}/fglrx-%{amdver}/archive_files/arch/x86/usr
%endif

      install -m755 X11R6/bin/* %{buildroot}/usr/bin
      install -m755 sbin/* %{buildroot}/usr/bin
      install -m755 X11R6/%{libpath}/fglrx/fglrx-libGL.so.1.2 %{buildroot}/usr/lib/fglrx
      install -m755 X11R6/%{libpath}/libAMDXvBA.so.1.0 %{buildroot}/usr/lib
      ln -snf libAMDXvBA.so.1.0 %{buildroot}/usr/lib/libAMDXvBA.so.1
      ln -snf libAMDXvBA.so.1.0 %{buildroot}/usr/lib/libAMDXvBA.so
      install -m755 X11R6/%{libpath}/libatiadlxx.so %{buildroot}/usr/lib
      install -m755 X11R6/%{libpath}/libfglrx_dm.so.1.0 %{buildroot}/usr/lib
      install -m755 X11R6/%{libpath}/libXvBAW.so.1.0 %{buildroot}/usr/lib
      ln -snf libXvBAW.so.1.0 %{buildroot}/usr/lib/libXvBAW.so.1
      ln -snf libXvBAW.so.1.0 %{buildroot}/usr/lib/libXvBAW.so
      ln -snf /usr/lib/libXvBAW.so.1.0 %{buildroot}/usr/lib/dri/fglrx_drv_video.so #omega 14.12
      install -m644 X11R6/%{libpath}/*.a %{buildroot}/usr/lib
      install -m644 X11R6/%{libpath}/*.cap %{buildroot}/usr/lib
      install -m755 X11R6/%{libpath}/modules/dri/*.so %{buildroot}/usr/lib/xorg/modules/dri
      install -m755 %{libpath}/*.so* %{buildroot}/usr/lib

      ln -snf /usr/lib/xorg/modules/dri/fglrx_dri.so %{buildroot}/usr/lib/dri/fglrx_dri.so
      ln -snf libfglrx_dm.so.1.0 %{buildroot}/usr/lib/libfglrx_dm.so.1
      ln -snf libfglrx_dm.so.1.0 %{buildroot}/usr/lib/libfglrx_dm.so
      ln -snf libatiuki.so.1.0 %{buildroot}/usr/lib/libatiuki.so.1
      ln -snf libatiuki.so.1.0 %{buildroot}/usr/lib/libatiuki.so

     # provided in opencl-catalyst package
     # rm %{buildroot}/usr/lib/lib{amdocl*,OpenCL}.so* 

      cd %{_builddir}/fglrx-%{amdver}/archive_files/common/
     patch -Np2 -i %{_sourcedir}/arch-fglrx-authatieventsd_new.patch
 #	
      install -m644 etc/ati/* %{buildroot}/etc/ati
      chmod 755 %{buildroot}/etc/ati/authatieventsd.sh

      install -m644 etc/security/console.apps/amdcccle-su %{buildroot}/etc/security/console.apps

      install -m755 usr/X11R6/bin/* %{buildroot}/usr/bin
      install -m644 usr/include/GL/*.h %{buildroot}/usr/include/GL
      install -m755 usr/sbin/*.sh %{buildroot}/usr/bin
      install -m644 usr/share/ati/amdcccle/* %{buildroot}/usr/share/ati/amdcccle
      install -m644 usr/share/icons/*.xpm %{buildroot}/usr/share/pixmaps
      install -m644 usr/share/man/man8/*.8 %{buildroot}/usr/share/man/man8
      install -m644 usr/share/applications/*.desktop %{buildroot}/usr/share/applications

    # ACPI example files
      install -m755 usr/share/doc/fglrx/examples/etc/acpi/*.sh %{buildroot}/etc/acpi
      sed -i -e "s/usr\/X11R6/usr/g" %{buildroot}/etc/acpi/ati-powermode.sh
      install -m644 usr/share/doc/fglrx/examples/etc/acpi/events/* %{buildroot}/etc/acpi/events

    # Add ATI Events Daemon launcher
      install -m755 %{SOURCE2} %{buildroot}/etc/rc.d/atieventsd
      install -m644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system

    # thanks to cerebral, we dont need that damned symlink
      install -m755 %{SOURCE1} %{buildroot}/etc/profile.d

    # License
      install -m644 %{_builddir}/fglrx-%{amdver}/archive_files/LICENSE.TXT %{buildroot}/usr/share/licenses/%{name}
      install -m644 %{_builddir}/fglrx-%{amdver}/archive_files/common/usr/share/doc/amdcccle/ccc_copyrights.txt \
	%{buildroot}/usr/share/licenses/%{name}/amdcccle_copyrights.txt

      install -m755 -d %{buildroot}/etc/modules-load.d
      install -m644 %{SOURCE4} %{buildroot}/etc/modules-load.d

    #workaround for the high io bug , thanks to lano1106 for finding this ugly bug! https://bbs.archlinux.org/viewtopic.php?pid=1279977#p1279977
      install -m755 %{SOURCE9} %{buildroot}/usr/bin
      install -m644 %{SOURCE10} %{buildroot}/usr/lib/systemd/system


## catalyst-hook section
      cd %{_builddir}/fglrx-%{amdver}/archive_files
      patch -Np1 -i %{_sourcedir}/makefile_compat.patch
      patch -Np1 -i %{_sourcedir}/lano1106_fglrx_intel_iommu.patch
      patch -Np1 -i %{_sourcedir}/lano1106_kcl_agp_13_4.patch
      patch -Np1 -i %{_sourcedir}/lano1106_fglrx-13.8_proc.patch
      patch -Np1 -i %{_sourcedir}/cold-fglrx-3.14-current_euid.patch
      patch -Np1 -i %{_sourcedir}/fglrx_3.17rc6-no_hotplug.patch
      
%ifarch i686 
patch -Np1 -i %{_sourcedir}/fglrx_gpl_symbol.patch
%endif

    # Prepare modules source files
      install -m755 -d %{buildroot}/usr/share/ati/build_mod
      install -m644 common/lib/modules/fglrx/build_mod/*.c \
                %{buildroot}/usr/share/ati/build_mod
      install -m644 common/lib/modules/fglrx/build_mod/*.h \
                %{buildroot}/usr/share/ati/build_mod
      install -m644 common/lib/modules/fglrx/build_mod/2.6.x/Makefile \
                %{buildroot}/usr/share/ati/build_mod
      install -m644 arch/%{archdir}/lib/modules/fglrx/build_mod/libfglrx_ip.a \
                %{buildroot}/usr/share/ati/build_mod
      install -m755 %{SOURCE12} %{buildroot}/usr/bin

    # modified ati's make.sh script
      install -m755 %{SOURCE13} %{buildroot}/usr/share/ati/build_mod

    # hook fglrx
      install -m755 -d %{buildroot}/usr/lib/initcpio/install
      install -m644 %{SOURCE11} %{buildroot}/usr/lib/initcpio/install/fglrx

    # systemd service to perform fglrx module build at shutdown
      install -m755 -d %{buildroot}/usr/lib/systemd/system
      install -m644 %{SOURCE14} %{buildroot}/usr/lib/systemd/system

# Remove rpaths 
chrpath --delete %{buildroot}/usr/bin/amdnotifyui
chrpath --delete %{buildroot}/usr/bin/amdcccle


%files
%{_sysconfdir}/acpi/ati-powermode.sh
%{_sysconfdir}/acpi/events/a-ac-aticonfig
%{_sysconfdir}/acpi/events/a-lid-aticonfig
%{_sysconfdir}/ati/amdpcsdb.default
%{_sysconfdir}/ati/atiapfxx
%{_sysconfdir}/ati/atiapfxx.blb
%{_sysconfdir}/ati/atiapfxx.log
%{_sysconfdir}/ati/authatieventsd.sh
%{_sysconfdir}/ati/control
%{_sysconfdir}/ati/logo.xbm.example
%{_sysconfdir}/ati/logo_mask.xbm.example
%{_sysconfdir}/ati/signature
%{_sysconfdir}/modules-load.d/catalyst.conf
%{_sysconfdir}/profile.d/catalyst.sh
%{_sysconfdir}/rc.d/atieventsd
%{_sysconfdir}/security/console.apps/amdcccle-su

%{_bindir}/amd-console-helper
%{_bindir}/amdcccle
%{_bindir}/amdnotifyui
%{_bindir}/amdupdaterandrconfig
%{_bindir}/amdxdg-su
%{_bindir}/aticonfig
%{_bindir}/atieventsd
%{_bindir}/atigetsysteminfo.sh
%{_bindir}/atiodcli
%{_bindir}/atiode
%{_bindir}/fgl_glxgears
%{_bindir}/fglrxinfo
%{_bindir}/temp_links_catalyst
%{_includedir}/GL/glATI.h
%{_includedir}/GL/glxATI.h
/usr/lib/dri/fglrx_dri.so
/usr/lib/dri/fglrx_drv_video.so
/usr/lib/fglrx/fglrx-libGL.so.1.2
/usr/lib/fglrx/switchlibGL
/usr/lib/fglrx/switchlibglx
/usr/lib/libAMDXvBA.cap
/usr/lib/libAMDXvBA.so
/usr/lib/libAMDXvBA.so.1
/usr/lib/libAMDXvBA.so.1.0
/usr/lib/libXvBAW.so
/usr/lib/libXvBAW.so.1
/usr/lib/libXvBAW.so.1.0
%ifarch x86_64
/usr/lib/libamdhsasc64.so
%else
/usr/lib/libamdhsasc32.so
%endif
/usr/lib/libatiadlxx.so
/usr/lib/libaticalcl.so
/usr/lib/libaticaldd.so
/usr/lib/libaticalrt.so
/usr/lib/libatiuki.so
/usr/lib/libatiuki.so.1
/usr/lib/libatiuki.so.1.0
/usr/lib/libfglrx_dm.a
/usr/lib/libfglrx_dm.so
/usr/lib/libfglrx_dm.so.1
/usr/lib/libfglrx_dm.so.1.0
/usr/lib/systemd/system/atieventsd.sh
/usr/lib/systemd/system/temp-links-catalyst.service
/usr/lib/xorg/modules/amdxmm.so
/usr/lib/xorg/modules/dri/fglrx_dri.so
/usr/lib/xorg/modules/drivers/fglrx_drv.so
/usr/lib/xorg/modules/extensions/fglrx/fglrx-libglx.so
/usr/lib/xorg/modules/glesx.so
/usr/lib/xorg/modules/linux/libfglrxdrm.so
%{_datadir}/applications/amdcccle.desktop
%{_datadir}/applications/amdccclesu.desktop
%{_datadir}/ati/amdcccle/
%{_datadir}/licenses/catalyst-utils/LICENSE.TXT
%{_datadir}/licenses/catalyst-utils/amdcccle_copyrights.txt
%{_datadir}/man/man8/atieventsd.8.gz
%{_datadir}/pixmaps/ccc_large.xpm

%files -n catalyst-libgl
/usr/lib/xorg/modules/extensions/libglx.so
/usr/lib/fglrx/libGL.so.1.2.0
/usr/lib/fglrx/libGL.so.1
/usr/lib/fglrx/libGL.so
/usr/lib/libGL.so.1.2.0
/usr/lib/libGL.so.1
/usr/lib/libGL.so
/usr/lib/libEGL.so.1.0.0
/usr/lib/libEGL.so.1
/usr/lib/libEGL.so
/usr/lib/libGLESv1_CM.so.1.1.0
/usr/lib/libGLESv1_CM.so.1
/usr/lib/libGLESv1_CM.so
/usr/lib/libGLESv2.so.2.0.0
/usr/lib/libGLESv2.so.2
/usr/lib/libGLESv2.so
%{_bindir}/pxp_switch_catalyst

%files -n opencl-catalyst
%{_sysconfdir}/OpenCL/vendors
/usr/lib/libamdocl*.so
/usr/lib/libOpenCL.so.1
/usr/lib/libOpenCL.so
%{_bindir}/clinfo

%files -n catalyst-hook
%{_datadir}/ati/build_mod
%{_bindir}/catalyst_build_module
/usr/lib/initcpio/install/fglrx
/usr/lib/systemd/system/catalyst-hook.service


%changelog

* Fri Jan 16 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 14.12-1
- For testing purposes
- Initial build
- A fork of PKGBUILD AUR Arch Linux thanks to Vi0L0 <vi0l093 AT gmail DOT com>
