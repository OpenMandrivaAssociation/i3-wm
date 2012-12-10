%global real_name i3
%global bugfix_release bf2
#% global upstream_version 3.e-%{bugfix_release}
%global upstream_version 4.3

Name:           i3-wm
#Version:        3.e.%{bugfix_release}
Version:        4.3
Release:        1
Summary:        Improved tiling window manager
License:        BSD
Group:          System/X11
URL:            http://i3.zekjur.net

Source0:        http://i3.zekjur.net/downloads/%{real_name}-%{upstream_version}.tar.bz2
Source1:        %{real_name}-logo.svg
source2:				.abf.yml
patch0:					i3-4.3.libev.patch

BuildRequires:  pkgconfig(libev)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(yajl)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  xcb-util-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  asciidoc
BuildRequires:  graphviz
BuildRequires:  bzip2
buildrequires:	pkgconfig(xcb-keysyms)
buildrequires:	pkgconfig(xcb-icccm)
buildrequires:	pkgconfig(pango)
buildrequires:	pkgconfig(pangocairo)
buildrequires:	pkgconfig(libstartup-notification-1.0)
buildrequires:	pkgconfig(xcursor)

Requires:       rxvt-unicode
Requires:       x11-apps
Suggests:       dmenu
Suggests:	i3-doc

%description
i3 is a tiling window manager, completely written from scratch.

Key features of i3 are correct handling multi-monitor, horizontal and
vertical columns (table abstraction) in tiling. It also provides
hooks/callbacks for other programs to integrate and it is UTF-8
clean. i3 uses xcb for asynchronous communication with X11, and has
several measures to be very fast.

Please be aware that i3 is primarily targeted at advanced users and
developers.


%package doc
Summary:        i3 window manager documentation
Group:          System/X11
BuildRequires:  doxygen
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Asciidoc and doxygen documentations for i3.


%prep
%setup -q -n %{real_name}-%{upstream_version}
%patch0 -p1 -b .libev
sed \
    -e 's|CFLAGS += -Wall|CFLAGS += %{optflags}|g' \
    -e 's|CFLAGS += -pipe|CFLAGS += -I/usr/include/libev |g' \
    -e 's|CFLAGS += -I/usr/local/include|CFLAGS += -I%{_includedir}|g' \
    -e 's|/usr/local/lib|%{_libdir}|g' \
    -e 's|.SILENT:||g' \
    -i common.mk


%build
make %{?_smp_mflags} V=1
cd man
make %{?_smp_mflags} V=1
cd ../docs
make %{?_smp_mflags} V=1
cd ..
doxygen pseudo-doc.doxygen
mv pseudo-doc/html pseudo-doc/doxygen


%install

make install \
     DESTDIR=%{buildroot} \
     INSTALL="install -p"

mkdir -p %{buildroot}/%{_mandir}/man1/
install -Dpm0644 man/*.1 \
        %{buildroot}/%{_mandir}/man1/

mkdir -p %{buildroot}/%{_datadir}/pixmaps/
install -Dpm0644 %{SOURCE1} \
        %{buildroot}/%{_datadir}/pixmaps/

%files
%defattr(-,root,root,-)
%doc LICENSE RELEASE-NOTES-%{upstream_version}
%{_bindir}/%{real_name}*
%{_includedir}/%{real_name}/*
%dir %{_sysconfdir}/%{real_name}/
%config(noreplace) %{_sysconfdir}/%{real_name}/config
%config(noreplace) %{_sysconfdir}/%{real_name}/config.keycodes
%{_datadir}/xsessions/%{real_name}.desktop
%{_mandir}/man*/%{real_name}*
%{_datadir}/pixmaps/%{real_name}-logo.svg
%{_datadir}/applications/%{real_name}.desktop


%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,png} pseudo-doc/doxygen/


%changelog
* Fri Feb 18 2011 Joao Victor Duarte Martins <jvdm@mandriva.com.br> 3.e.bf2-1mdv2011.0
+ Revision: 638328
- fix BuildRoot and add bzip2 to BuildRequires
- fix group tag
- fix package name and rename spec file
- First initial commit.
- create i3-wm

