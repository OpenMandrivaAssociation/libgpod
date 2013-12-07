%define	api	1.0
%define	major	4
%define libname %mklibname gpod %{major}
%define	devname	%mklibname -d gpod
%ifarch %arm
%bcond_with	sharp
%endif

Summary:	Library to access an iPod audio player
Name:		libgpod
Version:	0.8.2
Release:	8
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtkpod.org/
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2

BuildRequires:	eject
BuildRequires:	intltool
BuildRequires:	sg3_utils-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libimobiledevice-1.0)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(udev)

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Library to access an iPod audio player
Requires:	eject
#gw this is needed to have the udev script started after connecting an ipod
Requires:	%{name} >= %{EVRD}

%description -n	%{libname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n	%{devname}
Group:		Development/C
Summary:	Library to access an iPod audio player
Requires:	%{libname} = %{EVRD}
%if %{with sharp}
Requires:	%{name}-sharp = %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n	python-gpod
Group:		Development/Python
Summary:	Python module for iPod access
BuildRequires:	docbook-dtd412-xml
BuildRequires:	mutagen
BuildRequires:	swig
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(python)
Requires:	mutagen

%description -n	python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.
%if %{with sharp}
%package	sharp
Group:		Development/Other
Summary:	Mono binding to libgpod for iPod access
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
Requires:	%{libname} = %{EVRD}

%description	sharp
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Mono binding for libgpod.
%endif

%prep 
%setup -q
%apply_patches

%build
export LIBS='-lpython2.7'
%configure2_5x \
	--disable-static \
	--enable-udev \
	--without-hal 

%make 

%install
%makeinstall_std
%find_lang %{name}

%files -f %{name}.lang
%doc README* AUTHORS
%{_bindir}/ipod-read-sysinfo-extended
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/90-libgpod.rules

%files -n %{libname}
%{_libdir}/libgpod.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_libdir}/libgpod.so
%{_libdir}/pkgconfig/libgpod-%{api}.pc
%{_libdir}/pkgconfig/libgpod-sharp.pc
%{_includedir}/gpod-%{api}/
%{_datadir}/gtk-doc/html/*

%files -n python-gpod
%{py_platsitedir}/gpod/

%if %{with sharp}
%files sharp
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/libgpod-sharp*
%endif

