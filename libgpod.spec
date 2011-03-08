%define name libgpod
%define version 0.8.0
%define git 20100829
%define release %mkrel 2
%define major 4
%define libname %mklibname gpod %major
%define libnamedev %mklibname -d gpod
%define api 1.0
%define build_hal 0
%if %mdvver < 201100
%define build_hal 1
%endif
Summary: Library to access an iPod audio player
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.gz
License: LGPLv2+
Group: System/Libraries
Url: http://www.gtkpod.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: udev-devel dbus-glib-devel
%if %build_hal 
BuildRequires: hal-devel
%endif
BuildRequires: libsgutils-devel
BuildRequires: taglib-devel
BuildRequires: libxml2-devel
BuildRequires: libsqlite3-devel
BuildRequires: libusb1-devel
BuildRequires: libimobiledevice-devel
BuildRequires: gtk-doc
BuildRequires: eject
BuildRequires: intltool

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libname
Group: System/Libraries
Summary: Library to access an iPod audio player
Requires: eject
Requires: %name >= %version-release

%description -n %libname
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libnamedev
Group: Development/C
Summary: Library to access an iPod audio player
Requires: %libname = %version-%release
Requires: %name-sharp = %version-%release
Provides: %name-devel = %version-%release
Obsoletes: %mklibname -d gpod 2

%description -n %libnamedev
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n python-gpod
Group: Development/Python
Summary: Python module for iPod access
BuildRequires: python-gobject-devel
%py_requires -d
BuildRequires: mutagen
BuildRequires: swig
BuildRequires: docbook-dtd412-xml
Requires: mutagen
Requires: %libname = %version-%release

%description -n python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.

%package sharp
Group: Development/Other
Summary: Mono binding to libgpod for iPod access
BuildRequires: mono-devel
BuildRequires: gtk-sharp2
BuildRequires: gtk-sharp2-devel
Requires: %libname = %version-%release

%description sharp
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Mono binding for libgpod.

%prep 
%setup -q -n %{name}-%version
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
%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README* AUTHORS
%_bindir/ipod-read-sysinfo-extended
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/90-libgpod.rules
%if %build_hal
%_libdir/hal/scripts/*
%_datadir/hal/fdi/policy/20thirdparty/*
%endif

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%doc ChangeLog
%_libdir/lib*.so
%attr(644,root,root)  %_libdir/lib*a
%_libdir/pkgconfig/libgpod-%api.pc
%_libdir/pkgconfig/libgpod-sharp.pc
%_includedir/gpod-%api/
%_datadir/gtk-doc/html/*

%files -n python-gpod
%defattr(-,root,root)
%py_platsitedir/gpod/

%files sharp
%defattr(-,root,root)
%dir %_libdir/%name/
%_libdir/%name/libgpod-sharp*
