%define name libgpod
%define version 0.6.0
%define release %mkrel 2
%define major 3
%define libname %mklibname gpod %major
%define libnamedev %mklibname -d gpod

Summary: Library to access an iPod audio player
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.gz
License: LGPL
Group: System/Libraries
Url: http://www.gtkpod.org/
BuildRequires: gtk+2-devel
BuildRequires: hal-devel dbus-glib-devel
BuildRequires: libsgutils-devel
BuildRequires: taglib-devel
BuildRequires: eject
BuildRequires: perl-XML-Parser

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libname
Group: System/Libraries
Summary: Library to access an iPod audio player
Requires: eject
Requires: %name >= %version

%description -n %libname
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libnamedev
Group: Development/C
Summary: Library to access an iPod audio player
Requires: %libname = %version
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
BuildRequires: python-devel 
BuildRequires: mutagen
BuildRequires: swig
Requires: mutagen

%description -n python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
%find_lang %name
%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%_libdir/hal/libgpod-callout
%_bindir/ipod-read-sysinfo-extended
%_datadir/hal/fdi/policy/20thirdparty/*

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/lib*.so
%attr(644,root,root)  %_libdir/lib*a
%_libdir/pkgconfig/*.pc
%_includedir/gpod-1.0/
%_datadir/gtk-doc/html/*

%files -n python-gpod
%defattr(-,root,root)
%py_platsitedir/gpod/


