# TODO
# - the x11 libraires packaged to %{_libdir}/NX aren't used, still links (without rpath) to system xorg libs
#   so get rid of the copies or make link with them!
%define		agent_minor	10
%define		auth_minor	1
%define		comp_minor	3
%define		compext_minor	3
%define	 	compshad_minor	3
%define		proxy_minor	2
%define		win_minor	2
%define		X11_minor	5
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl.UTF-8):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	3.3.0
Release:	3
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/sources.php
Source0:	http://web04.nomachine.com/download/%{version}/sources/%{name}-X11-%{version}-%{X11_minor}.tar.gz
# Source0-md5:	6dae2fddc8081d30530f68e806105fd7
Source1:	http://web04.nomachine.com/download/%{version}/sources/%{name}agent-%{version}-%{agent_minor}.tar.gz
# Source1-md5:	7abd7812428aebcc48b996bcb5f1970b
Source2:	http://web04.nomachine.com/download/%{version}/sources/%{name}auth-%{version}-%{auth_minor}.tar.gz
# Source2-md5:	6d59de2cbf61430ac513ddfa6b05bc76
Source3:	http://web04.nomachine.com/download/%{version}/sources/%{name}proxy-%{version}-%{proxy_minor}.tar.gz
# Source3-md5:	047206e5a811b915aac4ae09bddef207
Source4:	http://web04.nomachine.com/download/%{version}/sources/%{name}comp-%{version}-%{comp_minor}.tar.gz
# Source4-md5:	2327cca8e6116fd6a96345566336d81d
Source5:	http://web04.nomachine.com/download/%{version}/sources/%{name}compext-%{version}-%{compext_minor}.tar.gz
# Source5-md5:	f138420fc7a005495675146a1e1539f2
Source6:	http://web04.nomachine.com/download/%{version}/sources/%{name}compshad-%{version}-%{compshad_minor}.tar.gz
# Source6-md5:	02f051366c4aae96bfefda60d701d8b4
Source7:	http://web04.nomachine.com/download/%{version}/sources/%{name}win-%{version}-%{win_minor}.tar.gz
# Source7-md5:	71de8e60c0cdee887e00d1a44f337ad1
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
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-util-imake
Requires:	nxcomp >= %{version}.%{comp_minor}
Requires:	nxcompext >= %{version}.%{compext_minor}
Requires:	nxcompshad >= %{version}.%{compshad_minor}
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc
Requires:	xorg-font-font-misc-misc-base
Provides:	nx-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't satisfy xorg deps for the rest of the distro
%define		_noautoprovfiles	%{_libdir}/NX

# and as we don't provide them, don't require either
%define		_noautoreq libX11.so libXext.so libXrender.so

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

%description -l pl.UTF-8
NoMachine NX to schemat kompresji dla X nowej generacji. Działa na
zdalnych sesjach X11 nawet przy prędkosci 56k albo większej.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6 -a7

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

%{__make} -C nx-X11 World

# build Extended Compression Library
cd nxcompext
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/{pkgconfig,NX},%{_bindir}}

# X11
install nx-X11/lib/X11/libX11.so.6.2 nx-X11/lib/Xext/libXext.so.6.4 nx-X11/lib/Xrender/libXrender.so.1.2.2 $RPM_BUILD_ROOT%{_libdir}/NX
install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig %{_libdir}/NX

%postun
/sbin/ldconfig %{_libdir}/NX

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/NX
%attr(755,root,root) %{_libdir}/NX/*.so.*
