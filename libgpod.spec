%define	api	1.0
%define	build_hal 0
%if %mdvver < 201100
%define build_hal 1
%endif
Summary:	Library to access an iPod audio player
Name:		libgpod
Version:	0.8.2
Release:	%mkrel 2
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtkpod.org/
BuildRequires:	gtk+2-devel
BuildRequires:	udev-devel dbus-glib-devel
%if %build_hal 
BuildRequires:	hal-devel
%endif
BuildRequires:	sg3_utils-devel
BuildRequires:	taglib-devel
BuildRequires:	libxml2-devel
BuildRequires:	sqlite3-devel
BuildRequires:	usb1.0-devel
BuildRequires:	libimobiledevice-devel
BuildRequires:	gtk-doc
BuildRequires:	eject
BuildRequires:	intltool

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%define	major	4
%define libname %{mklibname gpod %{major}}
%package -n	%{libname}
Group:		System/Libraries
Summary:	Library to access an iPod audio player
Requires:	eject
#gw this is needed to have the udev script started after connecting an ipod
Requires:	%name >= %version

%description -n	%{libname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%define	devname	%{mklibname -d gpod}
%package -n	%{devname}
Group:		Development/C
Summary:	Library to access an iPod audio player
Requires:	%{libname} = %{EVRD}
Requires:	%{name}-sharp = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname -d gpod 2}

%description -n	%{devname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n	python-gpod
Group:		Development/Python
Summary:	Python module for iPod access
BuildRequires:	python-gobject-devel
BuildRequires:	python-devel
BuildRequires:	mutagen
BuildRequires:	swig
BuildRequires:	docbook-dtd412-xml
Requires:	mutagen

%description -n	python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.

%package	sharp
Group:		Development/Other
Summary:	Mono binding to libgpod for iPod access
BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2
BuildRequires:	gtk-sharp2-devel
Requires:	%{libname} = %{EVRD}

%description	sharp
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Mono binding for libgpod.

%prep 
%setup -q
%apply_patches

%build
%configure2_5x --enable-gtk-doc --enable-udev \
%if !%build_hal
	--without-hal 
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
%find_lang %{name}

%files -f %{name}.lang
%doc README* AUTHORS
%{_bindir}/ipod-read-sysinfo-extended
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/90-libgpod.rules
%if %{build_hal}
# %{_libdir}/hal/scripts/*
# %{_datadir}/hal/fdi/policy/20thirdparty/*
%endif

%files -n %{libname}
%{_libdir}/libgpod.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_libdir}/libgpod.so
%{_libdir}/libgpod.*a
%{_libdir}/pkgconfig/libgpod-%{api}.pc
%{_libdir}/pkgconfig/libgpod-sharp.pc
%{_includedir}/gpod-%{api}/
%{_datadir}/gtk-doc/html/*

%files -n python-gpod
%{py_platsitedir}/gpod/

%files sharp
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/libgpod-sharp*


%changelog
* Wed Oct 26 2011 Götz Waschk <waschk@mandriva.org> 0.8.2-2
+ Revision: 707253
- rebuild for new libpng

  + Zombie Ryushu <ryushu@mandriva.org>
    - scripts for 2010.1
    - Fix release tag

* Sun Jul 24 2011 Götz Waschk <waschk@mandriva.org> 0.8.2-1
+ Revision: 691405
- new version

* Thu May 12 2011 Götz Waschk <waschk@mandriva.org> 0.8.0-6
+ Revision: 673974
- readd dep on main package to lib package
- clean buildroot before installation

* Tue May 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.0-5
+ Revision: 673265
- cleanups
- untangle dependency loop

* Sat Apr 30 2011 Funda Wang <fwang@mandriva.org> 0.8.0-4
+ Revision: 661019
- fix requires on libpackage

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8.0-3
+ Revision: 660259
- mass rebuild

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added missing BuildRequires: docbook-dtd412-xml, otherwise build hangs

* Mon Nov 01 2010 Götz Waschk <waschk@mandriva.org> 0.8.0-2mdv2011.0
+ Revision: 591430
- build with hal for future backports
- rebuild for python 2.7

* Tue Oct 12 2010 Götz Waschk <waschk@mandriva.org> 0.8.0-1mdv2011.0
+ Revision: 585134
- update to new version 0.8.0

* Wed Sep 29 2010 Götz Waschk <waschk@mandriva.org> 0.7.95-1mdv2011.0
+ Revision: 582071
- new version
- drop patch

* Fri Sep 10 2010 Götz Waschk <waschk@mandriva.org> 0.7.94-3mdv2011.0
+ Revision: 577066
- add missing automake call

* Fri Sep 10 2010 Götz Waschk <waschk@mandriva.org> 0.7.94-2mdv2011.0
+ Revision: 577065
- fix libgpod-sharp dll map
- update python dep

* Wed Sep 01 2010 Götz Waschk <waschk@mandriva.org> 0.7.94-1mdv2011.0
+ Revision: 575012
- new version
- add mono bindings

* Tue Apr 06 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.7.93-1mdv2010.1
+ Revision: 532378
- libgpod 0.7.93

* Mon Mar 22 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.7.92-2mdv2010.1
+ Revision: 526326
- rebuild against new libimobiledevice

* Fri Mar 19 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.7.92-1mdv2010.1
+ Revision: 525233
- libgpod 0.7.92

  + Götz Waschk <waschk@mandriva.org>
    - add all README files and move ChangeLog to the devel package

* Tue Mar 02 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.7.91-1mdv2010.1
+ Revision: 513548
- 0.7.91

* Fri Feb 05 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.7.90-1mdv2010.1
+ Revision: 501129
- libgpod 0.7.90:
- nano5g and iphone support \o/

* Wed Dec 09 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.7.2-2mdv2010.1
+ Revision: 475359
- add patch to fix non-working nano 4g black

* Fri Apr 24 2009 Götz Waschk <waschk@mandriva.org> 0.7.2-1mdv2010.0
+ Revision: 368991
- new version
- fix installation

  + Christophe Fergeau <cfergeau@mandriva.com>
    - add libxml2 to buildrequires

* Mon Jan 19 2009 Götz Waschk <waschk@mandriva.org> 0.7.0-1mdv2009.1
+ Revision: 331104
- new version
- new major
- drop all patches
- fix build deps

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 0.6.0-6mdv2009.1
+ Revision: 319223
- rediff ipod patch
- rebuild for new python

* Wed Jul 30 2008 Götz Waschk <waschk@mandriva.org> 0.6.0-5mdv2009.0
+ Revision: 254898
- fix build with libsgutils2
- fix missing header
- update license

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Mar 20 2008 Götz Waschk <waschk@mandriva.org> 0.6.0-4mdv2008.1
+ Revision: 189130
- fix several bugs with patches from svn

* Thu Feb 21 2008 Götz Waschk <waschk@mandriva.org> 0.6.0-3mdv2008.1
+ Revision: 173501
- move hal callout to the right dir

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Götz Waschk <waschk@mandriva.org> 0.6.0-2mdv2008.1
+ Revision: 108087
- fix devel name

* Sun Nov 11 2007 Götz Waschk <waschk@mandriva.org> 0.6.0-1mdv2008.1
+ Revision: 108024
- fix buildrequires
- new version
- new major
- add new hal callout

* Sat Jun 23 2007 Götz Waschk <waschk@mandriva.org> 0.5.2-1mdv2008.0
+ Revision: 43402
- new version

* Mon Jun 18 2007 Götz Waschk <waschk@mandriva.org> 0.5.0-1mdv2008.0
+ Revision: 40887
- new version
- new major
- new python-gpod dep on mutagen


* Mon Jan 15 2007 Götz Waschk <waschk@mandriva.org> 0.4.2-2mdv2007.0
+ Revision: 109259
- just increase the release tag
- fix python path
- new version
- new major

* Thu Dec 14 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.4.0-3mdv2007.1
+ Revision: 97036
- Rebuild against new Python

  + Götz Waschk <waschk@mandriva.org>
    - fix python package on x86_64 (Colin Guthrie)
    - Import libgpod

* Sat Oct 07 2006 Götz Waschk <waschk@mandriva.org> 0.4.0-1mdv2007.1
- add python bindings
- fix buildrequires
- update file list
- New version 0.4.0

* Wed Aug 02 2006 Götz Waschk <waschk@mandriva.org> 0.3.2-2mdv2007.0
- fix buildrequires

* Sun Mar 05 2006 Götz Waschk <waschk@mandriva.org> 0.3.2-1mdk
- New release 0.3.2

* Wed Jan 25 2006 Götz Waschk <waschk@mandriva.org> 0.3.0-2mdk
- rebuild for new dbus

* Sun Dec 11 2005 Götz Waschk <waschk@mandriva.org> 0.3.0-1mdk
- New release 0.3.0
- use mkrel

* Sat Dec 03 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.0-3mdk
- add BuildRequires: perl-XML-Parser

* Thu Dec 01 2005 Frederic Crozat <fcrozat@mandriva.com> 0.2.0-2mdk
- Remove pmount dependency, it isn't needed at all

* Mon Nov 28 2005 Götz Waschk <waschk@mandriva.org> 0.2.0-1mdk
- initial package

