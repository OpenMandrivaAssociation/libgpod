%define	api	1.0
%define	build_hal 0
%if %mdvver < 201100
%define build_hal 1
%endif
Summary:	Library to access an iPod audio player
Name:		libgpod
Version:	0.8.2
Release:	%mkrel 1
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
%{_libdir}/hal/scripts/*
%{_datadir}/hal/fdi/policy/20thirdparty/*
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
