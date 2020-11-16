%global __requires_exclude perl\\(AnyEvent::I3\\)

%global real_name i3
%global bugfix_release bf2
%global upstream_version 4.18

Name:           i3-wm
Version:        4.19
Release:        1
Summary:        Improved tiling window manager
License:        BSD
Group:          System/X11
URL:            http://i3wm.org/

Source0:        http://i3wm.org/downloads/%{real_name}-%{version}.tar.xz
Source1:        %{real_name}-logo.svg
source2:				.abf.yml
#Patch1:		fix-ev.patch

BuildRequires: pkgconfig(libev)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(yajl)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: meson
BuildRequires: x11-proto-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: pkgconfig(libev)
BuildRequires: bison
BuildRequires: doxygen
BuildRequires: flex
BuildRequires: asciidoc
BuildRequires: graphviz
BuildRequires: bzip2
BuildRequires: pkgconfig(xcb-cursor)
Buildrequires: pkgconfig(xcb-keysyms)
Buildrequires: pkgconfig(xcb-icccm)
BuildRequires: pkgconfig(xcb-xrm)
Buildrequires: pkgconfig(pango)
Buildrequires: pkgconfig(pangocairo)
Buildrequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(libpcre)
Buildrequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(yajl)
BuildRequires: xmlto

Requires:       rxvt-unicode
Requires:       x11-apps
Recommends:     dmenu
Recommends:     i3-doc
Recommends:	i3status

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
%setup -q -n %{real_name}-%{version}
%autopatch -p1

%build
%meson

%meson_build -C *-openmandriva-linux-gnu*

doxygen pseudo-doc.doxygen
mv pseudo-doc/html pseudo-doc/doxygen

%install
%meson_install -C *-openmandriva-linux-gnu*

mkdir -p %{buildroot}/%{_mandir}/man1/
install -Dpm0644 man/*.1 %{buildroot}/%{_mandir}/man1/

%posttrans
if [ "$1" -eq 1 ]; then
	if [ -e %{_datadir}/xsessions/31i3.desktop ]; then
		rm -rf %{_datadir}/xsessions/31i3.desktop
	fi
	if [ -e %{_sysconfdir}/X11/dm/Sessions/31i3.desktop ]; then
		rm -rf %{_sysconfdir}/X11/dm/Sessions/31i3.desktop
	fi
fi

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/%{real_name}*
%{_includedir}/%{real_name}/*
%dir %{_sysconfdir}/%{real_name}/
%config(noreplace) %{_sysconfdir}/%{real_name}/config
%config(noreplace) %{_sysconfdir}/%{real_name}/config.keycodes
%{_datadir}/xsessions/*.desktop
%{_mandir}/man*/%{real_name}*
#{_datadir}/pixmaps/i3*
%{_datadir}/applications/*.desktop
%exclude %{_docdir}/i3/*


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

