%define		_agent_minor	8
%define		_auth_minor	1
%define		_comp_minor	7
%define		_compext_minor	1
%define	 	_compshad_minor	3
%define		_proxy_minor	1
%define		_X11_minor	2
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl.UTF-8):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	3.2.0
Release:	1.1
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/download/snapshot/nxsources/
Source0:	http://web04.nomachine.com/download/%{version}/sources/%{name}-X11-%{version}-%{_X11_minor}.tar.gz
# Source0-md5:	0a969199c77a604a488794c56176000f
Source1:	http://web04.nomachine.com/download/%{version}/sources/%{name}agent-%{version}-%{_agent_minor}.tar.gz
# Source1-md5:	ab4f771bc522caa0a86317dc882679e8
Source2:	http://web04.nomachine.com/download/%{version}/sources/%{name}auth-%{version}-%{_auth_minor}.tar.gz
# Source2-md5:	18519f2bcf30b10b766a60926fbe1017
Source3:	http://web04.nomachine.com/download/%{version}/sources/%{name}proxy-%{version}-%{_proxy_minor}.tar.gz
# Source3-md5:	ac31e8f2f112e3720f3c00cec67c0734
Source4:	http://web04.nomachine.com/download/%{version}/sources/%{name}comp-%{version}-%{_comp_minor}.tar.gz
# Source4-md5:	5ea64a557c770d9f5cc4b9a7a9d1343c
Source5:	http://web04.nomachine.com/download/%{version}/sources/%{name}compext-%{version}-%{_compext_minor}.tar.gz
# Source5-md5:	cd1296ebd24b1d7c4f82537a395ad6e8
Source6:	http://web04.nomachine.com/download/%{version}/sources/%{name}compshad-%{version}-%{_compshad_minor}.tar.gz
# Source6-md5:	6edfa4f65f579306f05af2451249c2bf
Patch0:		%{name}-X11-libs.patch
Patch1:		%{name}compext-libs.patch
Patch2:		%{name}viewer.patch
Patch3:		%{name}-gcc-4.1.patch
Patch4:		%{name}-fonts.patch
Patch5:		%{name}-system-nxcomp.patch
URL:		http://www.nomachine.com/
#BuildRequires:	Xaw3d-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	xorg-cf-files
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-util-imake
Requires:	nxcomp >= %{version}.%{_comp_minor}
Requires:	nxcompext >= %{version}.%{_compext_minor}
Requires:	nxcompshad >= %{version}.%{_compshad_minor}
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc
Requires:	xorg-font-font-misc-misc-base
Provides:	nx-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

%description -l pl.UTF-8
NoMachine NX to schemat kompresji dla X nowej generacji. Działa na
zdalnych sesjach X11 nawet przy prędkosci 56k albo większej.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6
#%patch0 -p1
#%patch1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p0
#%patch5 -p1

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CXXFLAGS="%{rpmcflags} -fPIC"
export CPPFLAGS="%{rpmcflags} -fPIC"

perl -pi -e"s|CXXFLAGS=.-O.*|CXXFLAGS=\"$CXXFLAGS\"|" */configure

# build Compression Library and Proxy
for i in nxcomp nxproxy nxcompshad; do
cd $i
%configure
%{__make}
cd ..
done

# build X11 Support Libraries and Agents

cd nx-X11
%{__make} World
cd ..

# build Extended Compression Library
cd nxcompext
%configure
%{__make}

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/pkgconfig,%{_bindir},%{_includedir}/nxcompsh}

# X11
install nx-X11/lib/X11/libX11.so \
	nx-X11/lib/Xext/libXext.so \
	nx-X11/lib/Xrender/libXrender.so \
	$RPM_BUILD_ROOT%{_libdir}
install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libX{11-nx.so.6,ext-nx.so.6,render-nx.so.1}

# install Compression Libraries and Proxy
cp -a nxcomp/libXcomp.so.* $RPM_BUILD_ROOT%{_libdir}
cp -a nxcompext/libXcompext.so.* $RPM_BUILD_ROOT%{_libdir}
cp -a nxcompshad/libXcompshad.so.* $RPM_BUILD_ROOT%{_libdir}

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.so.*
