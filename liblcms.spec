%define name liblcms
%define fname lcms
%define version 1.16
%define versioninfo 1:14:0
%define release %mkrel 1

%define lib_major 1
%define lib_name %mklibname %{fname} %{lib_major}

Name: %{name}
Summary: Little cms color engine
Version: %{version}
Release: %{release}
License: LGPL
Source0: http://www.littlecms.com/%{fname}-%{version}.tar.bz2
Patch0: %{name}-1.13-bigendian.patch
URL: http://www.littlecms.com
Group: Graphics
BuildRequires: tiff-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This is a CMM engine to deal with color management stuff. 

%package -n %{lib_name}
Summary: Little cms color engine
Group: System/Libraries
Obsoletes: %{name}
Provides: %{name} = %version-%release

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with liblcms.

%package -n %{lib_name}-devel
Summary:  Header files and static library for development with LCMS
Group: Development/C
Requires: %{lib_name} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{name}-devel
Provides: lcms-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package is only needed if you plan to develop or compile
applications which requires the LCMS library.

%prep
%setup -q -n %{fname}-%{version}
%patch0 -p1
chmod 644 doc/* AUTHORS COPYING INSTALL NEWS README.1ST

%build
%configure2_5x
%make 
make check

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir} \
	$RPM_BUILD_ROOT%{_includedir}/lcms \
	$RPM_BUILD_ROOT%{_datadir}/lcms-%{version}
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig -n %{lib_name}

%postun -p /sbin/ldconfig -n %{lib_name}

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING
%{_datadir}/lcms-%{version}
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README.1ST doc/LCMSAPI.TXT doc/TUTORIAL.TXT
%{_bindir}/*
%attr(644,root,root) %{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*


