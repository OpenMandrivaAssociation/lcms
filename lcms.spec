%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Color management library
Name:		lcms
Version:	1.19
Release:	18
License:	MIT
Group:		Graphics
Url:		http://www.littlecms.com/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		lcms-1.19-fix-python3.2.patch
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)

%description
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

%package -n	%{libname}
Summary:	The Shared library for "Little cms"
Group:		System/Libraries

%description -n	%{libname}
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

This package provides the shared lcms library.

%package -n	%{devname}
Summary:	Static library and header files for the "Little cms" library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} >= %{version}-%{release}

%description -n	%{devname}
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

This package contains the static lcms library and its header files.

%package -n	python2-lcms
Summary:	Python2 bindings for the lcms color management engine
Group:		Development/Python

%description -n	python2-lcms
python2-lcms is a Python2 module that interfaces to the lcms color management
engine.

%prep
%setup -q
%apply_patches
chmod 644 doc/* matlab/* AUTHORS COPYING NEWS README.1ST python/testbed/*

%build
%configure \
	--with-python \
	--disable-static

# regenerate the swig shit
pushd python
./swig_lcms
popd

%make

%check
make check

%install
%makeinstall_std

%files
%doc doc/* matlab/*.pdf
%{_bindir}/icc2ps
%{_bindir}/icclink
%{_bindir}/icctrans
%{_bindir}/jpegicc
%{_bindir}/tiffdiff
%{_bindir}/tifficc
%{_bindir}/wtpt
%{_mandir}/man1/icc2ps.1*
%{_mandir}/man1/icclink.1*
%{_mandir}/man1/jpegicc.1*
%{_mandir}/man1/tifficc.1*
%{_mandir}/man1/wtpt.1*

%files -n %{libname}
%doc AUTHORS COPYING NEWS README.1ST
%{_libdir}/liblcms.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lcms.pc

%files -n python2-lcms
%doc python/testbed/*
%{py2_platsitedir}/lcms.py
%{py2_platsitedir}/_lcms.so
