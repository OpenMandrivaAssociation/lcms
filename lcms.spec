%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Color management library
Name:		lcms
Version:	1.19
Release:	7
License:	MIT
Group:		Graphics
URL:		http://www.littlecms.com/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	autoconf automake libtool
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	python-devel
BuildRequires:	swig
BuildRequires:	zlib-devel
Conflicts:	%{mklibname lcms 1}-devel < 1.16

%description
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

%package -n	%{libname}
Summary:	The Shared library for "Little cms"
Group:		System/Libraries
Provides:	liblcms = %{version}
Obsoletes:	liblcms < 1.19-7

%description -n	%{libname}
Little cms is a color management library. Implements fast transforms between
ICC profiles. It is focused on speed, and is portable across several platforms.

This package provides the shared lcms library.

%package -n	%{develname}
Summary:	Static library and header files for the "Little cms" library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Obsoletes:	%{name}-devel < 1.19-7
Obsoletes:	%{mklibname lcms 1}-devel < 1.19-7
Requires:	%{libname} >= %{version}-%{release}

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

# fix attribs
chmod 644 doc/* matlab/* AUTHORS COPYING NEWS README.1ST python/testbed/*

%build
autoreconf -fi

%configure2_5x \
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
%doc AUTHORS COPYING NEWS README.1ST
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/lcms.pc

%files -n python-lcms
%doc python/testbed/*
%attr(0644,root,root) %{py_platsitedir}/lcms.py
%attr(0755,root,root) %{py_platsitedir}/_lcms.so

%changelog
* Thu Dec 22 2011 Oden Eriksson <oeriksson@mandriva.com> 1.19-6
+ Revision: 744409
- rebuilt against libtiff.so.5

* Sat Dec 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.19-5
+ Revision: 737553
- fix build
- one more fix
- drop the static lib and the libtool *.la file
- various fixes

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.19-4
+ Revision: 666063
- mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.19-3mdv2011.0
+ Revision: 627612
- don't force the usage of automake1.7

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.19-2mdv2011.0
+ Revision: 488775
- rebuilt against libjpeg v8

* Sun Dec 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.19-1mdv2010.1
+ Revision: 474134
- update to new version 1.19
- drop patch 0, fixed by upstream

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.18-3mdv2010.0
+ Revision: 416513
- rebuilt against libjpeg v7

* Mon May 25 2009 Rafael da Veiga Cabral <cabral@mandriva.com> 1.18-2mdv2010.0
+ Revision: 379553
- security fix for CVE-2009-0793
- added  lcms-1.18-CVE-2009-0793.patch (1.18a)
- security fix for CVE-2009-0793

* Thu Mar 26 2009 Frederik Himpe <fhimpe@mandriva.org> 1.18-1mdv2009.1
+ Revision: 361499
- Update to new version 1.18 (fixes CVE-2009-0723, CVE-2009-0733 and
  CVE-2009-0581)
- Remove bigendian patch: partly merged upstream, partly wrong (alpha on
  Linux uses little endian)
- Remove python patch: not needed

* Sat Dec 27 2008 Adam Williamson <awilliamson@mandriva.org> 1.17-6mdv2009.1
+ Revision: 319539
- rebuild with python 2.6

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.17-5mdv2009.1
+ Revision: 316260
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.17-4mdv2009.0
+ Revision: 225309
- swig-devel doesn't exist
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.17-3mdv2008.1
+ Revision: 170938
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.17-2mdv2008.1
+ Revision: 150441
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Aug 12 2007 Oden Eriksson <oeriksson@mandriva.com> 1.17-1mdv2008.0
+ Revision: 62196
- 1.17
- renaming it from liblcms to lcms
- rediffed P0
- added the python-lcms sub package + P1
- fix deps
- renaming it to lcms


* Sun Feb 18 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.16-1mdv2007.0
+ Revision: 122456
- Release: 1.16.

* Sun Jan 28 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.15-1mdv2007.1
+ Revision: 114523
- Import liblcms

* Sun Jan 28 2007 Götz Waschk <waschk@mandriva.org> 1.15-1mdv2007.1
- unpack patch

* Wed Apr 19 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.15-1mdk
- New release 1.15
- use mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.14-2mdk
- Rebuild

* Mon Jul 11 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.14-1mdk
- Release: 1.14.

* Tue Jun 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.13-1mdk
- Release: 1.13.
- Rebuilt Patch0.

