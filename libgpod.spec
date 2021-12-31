%define api 1.0
%define major 4
%define libname %mklibname gpod %{major}
%define devname %mklibname -d gpod
%define snapshot 0

%bcond_with	sharp
%bcond_with	python

Summary:	Library to access an iPod audio player
Name:		libgpod
Version:	0.8.3
%if %snapshot
Release:	0.%{snapshot}.5
Source0:	%name-%{snapshot}.tar.xz
%else
Release:	9
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2
%endif
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtkpod.org/
Patch0:		libplist-api-change.patch
Patch1:		libgpod-0.8.3-fix-segfault-and-some-typos.patch
Patch2:         0001-configure.ac-Add-support-for-libplist-2.2.patch

BuildRequires:	eject
BuildRequires:	intltool
BuildRequires:	sg3_utils-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libimobiledevice-1.0)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libplist-2.0) >= 2.2.0
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(udev)
BuildRequires:	gtk-doc

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library to access an iPod audio player
Requires:	eject
#gw this is needed to have the udev script started after connecting an ipod
Requires:	%{name} >= %{EVRD}

%description -n %{libname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %{devname}
Group:		Development/C
Summary:	Library to access an iPod audio player
Requires:	%{libname} = %{EVRD}
%if %{with sharp}
Requires:	%{name}-sharp = %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%if %{with python}
%package -n python-gpod
Group:		Development/Python
Summary:	Python module for iPod access
BuildRequires:	docbook-dtd412-xml
BuildRequires:	mutagen
BuildRequires:	swig
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(python)
Requires:	mutagen

%description -n python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.
%endif

%if %{with sharp}
%package sharp
Group:		Development/Other
Summary:	Mono binding to libgpod for iPod access
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
Requires:	%{libname} = %{EVRD}

%description sharp
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Mono binding for libgpod.
%endif

%prep
%autosetup -p1

autoreconf -fi
# Fix bogus reference
sed -i -e 's,docs/reference/xml,docs/reference,g' bindings/python/Makefile.am

%build
%if %snapshot
NOCONFIGURE=1 ./autogen.sh
%endif
%configure \
	--disable-static \
	--disable-more-warnings \
	--enable-udev \
	--without-hal \
	--disable-gtk-doc \
	--disable-gtk-doc-html \
	--disable-gtk-doc-pdf \
	--without-mono \
	--without-python

%make_build

%install
%make_install

%if !%{with sharp}
rm -rf %{buildroot}%{_libdir}/pkgconfig/libgpod-sharp.pc
%endif

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
%{_includedir}/gpod-%{api}/
%doc %{_datadir}/gtk-doc/html/%{name}

%if %{with python}
%files -n python-gpod
%{py2_platsitedir}/gpod/
%endif

%if %{with sharp}
%files sharp
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/libgpod-sharp*
%{_libdir}/pkgconfig/libgpod-sharp.pc
%endif
