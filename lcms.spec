%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Color management library
Name:		lcms
Version:	1.19
Release:	20
License:	MIT
Group:		Graphics
Url:		http://www.littlecms.com/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		lcms-1.19-fix-python3.2.patch
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(python2)
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
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} >= %{EVRD}

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
%autosetup -p1

find . -name \*.[ch] | xargs chmod -x
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT

%build
export PYTHON=%{__python2}
%configure \
	--with-python \
	--disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# regenerate the swig shit
cd python
./swig_lcms
cd -

%make_build

%check
make check

%install
%make_install

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
%{python2_sitearch}/lcms.py*
%{python2_sitearch}/_lcms.so
