%global real_name i3
%global bugfix_release bf2
%global upstream_version 3.e-%{bugfix_release}

Name:           i3-wm
Version:        3.e.%{bugfix_release}
Release:        %mkrel 1
Summary:        Improved tiling window manager
License:        BSD
Group:          System/X11
URL:            http://i3.zekjur.net

Source0:        http://i3.zekjur.net/downloads/%{real_name}-%{upstream_version}.tar.bz2
Source1:        %{real_name}-logo.svg

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  libev-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libx11-devel
BuildRequires:  libyajl-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  asciidoc
BuildRequires:  graphviz
BuildRequires:  bzip2

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
rm -rf %{buildroot}

make install \
     DESTDIR=%{buildroot} \
     INSTALL="install -p"

mkdir -p %{buildroot}/%{_mandir}/man1/
install -Dpm0644 man/*.1 \
        %{buildroot}/%{_mandir}/man1/

mkdir -p %{buildroot}/%{_datadir}/pixmaps/
install -Dpm0644 %{_sourcedir}/i3-logo.svg \
        %{buildroot}/%{_datadir}/pixmaps/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GOALS LICENSE RELEASE-NOTES-%{upstream_version}
%{_bindir}/%{real_name}*
%{_includedir}/%{real_name}/*
%dir %{_sysconfdir}/%{real_name}/
%config(noreplace) %{_sysconfdir}/%{real_name}/config
%config(noreplace) %{_sysconfdir}/%{real_name}/welcome
%{_datadir}/xsessions/%{real_name}.desktop
%{_mandir}/man*/%{real_name}*
%{_datadir}/pixmaps/i3-logo.svg


%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,png} pseudo-doc/doxygen/
