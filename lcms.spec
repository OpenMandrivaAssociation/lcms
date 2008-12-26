%define	major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Color management library
Name:		lcms
Version:	1.17
Release:	%mkrel 6
License:	MIT
Group:		Graphics
URL:		http://www.littlecms.com/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		liblcms-bigendian.diff
Patch1:		lcms-python.diff
BuildRequires:	automake1.7
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	python-devel
BuildRequires:	swig
BuildRequires:	zlib-devel
Conflicts:	%{mklibname %{name} 1}-devel < 1.16
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

%package -n	%{libname}
Summary:	The Shared library for "Little cms"
Group:          System/Libraries
Provides:	liblcms = %{version}
Obsoletes:	liblcms

%description -n	%{libname}
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

This package provides the shared lcms library.

%package -n	%{develname}
Summary:	Static library and header files for the "Little cms" library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	%{mklibname %{name} 1}-devel = %{version}
Obsoletes:	%{name}-devel
Obsoletes:	%{mklibname %{name} 1}-devel
Requires:	%{libname} = %{version}

%description -n	%{develname}
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

This package contains the static lcms library and its header files.

%package -n	python-lcms
Summary:	Python bindings for the lcms color management engine
Group:		Development/Python

%description -n	python-lcms
python-lcms is a Python module that interfaces to the lcms color management
engine.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

# fix attribs
chmod 644 doc/* matlab/* AUTHORS COPYING NEWS README.1ST python/testbed/*

%build
rm -f configure
libtoolize --force --copy; aclocal-1.7; automake-1.7 --add-missing --copy --foreign; autoconf

%configure2_5x \
    --with-python

# regenerate the swig shit
pushd python
    ./swig_lcms
popd

%make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -f %{buildroot}%{py_platsitedir}/*.a
rm -f %{buildroot}%{py_platsitedir}/*.la

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* matlab/*.pdf
%attr(0755,root,root) %{_bindir}/icc2ps
%attr(0755,root,root) %{_bindir}/icclink
%attr(0755,root,root) %{_bindir}/icctrans
%attr(0755,root,root) %{_bindir}/jpegicc
%attr(0755,root,root) %{_bindir}/tiffdiff
%attr(0755,root,root) %{_bindir}/tifficc
%attr(0755,root,root) %{_bindir}/wtpt
%attr(0644,root,root) %{_mandir}/man1/icc2ps.1*
%attr(0644,root,root) %{_mandir}/man1/icclink.1*
%attr(0644,root,root) %{_mandir}/man1/jpegicc.1*
%attr(0644,root,root) %{_mandir}/man1/tifficc.1*
%attr(0644,root,root) %{_mandir}/man1/wtpt.1*

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README.1ST
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_libdir}/pkgconfig/lcms.pc

%files -n python-lcms
%defattr(-,root,root)
%doc python/testbed/*
%attr(0644,root,root) %{py_platsitedir}/lcms.py
%attr(0755,root,root) %{py_platsitedir}/_lcms.so
