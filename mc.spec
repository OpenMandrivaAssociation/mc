# avoid dependency on X11 libraries
%define without_x       1

#define Werror_cflags %nil

Name:		mc
Version:	4.8.4
Release:	%mkrel 1
Summary:	A user-friendly file manager and visual shell
License:	GPLv2+
Group:		File tools
URL:		http://www.midnight-commander.org/
Source0:	http://www.midnight-commander.org/downloads/%{name}-%{version}.tar.xz

# ** Mandriva patches: 0 - 99 **

# (tv) add runlevel to initscript
Patch6:		mc-4.7.0-pre2-decent_defaults.patch
Patch9:		mc-4.8.0-xdg.patch
Patch11:	mc-4.7.0.2-do-not-mark-tabs.patch
Patch14:	mc-4.7.2-bash_history.patch

BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel
Buildrequires:	glib2-devel
BuildRequires:	pcre-devel
BuildRequires:	bison
%if %{without_x}
%else
BuildRequires:	X11-devel
%endif
BuildRequires:	gettext-devel
Requires:	groff

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.

%prep
%setup -q

%patch6 -p0 -b .decent_defaults
#patch9 -p1 -b .xdg
%patch11 -p0 -b .tabs
%patch14 -p1

%__sed -i 's:|hxx|:|hh|hpp|hxx|:' misc/syntax/Syntax

%build
autoreconf -fi
%serverbuild
export X11_WWW="www-browser"

%configure2_5x \
    --with-debug \
    --enable-dependency-tracking \
    --without-included-gettext \
    --without-included-slang \
    --with-screen=slang \
    --with-search-engine=glib \
    --enable-nls \
    --enable-charset \
    --enable-largefile \
    --disable-rpath \
    --with-mcfs \
    --enable-extcharset \
    --with-ext2undel \
    --with-mmap \
%if %{without_x}
    --without-x
%endif

%make

%install
#fix mc-wrapper.sh
%__perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall_std

%__install -m644 contrib/mc.sh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.sh
%__install -m644 contrib/mc.csh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.csh

%find_lang %{name} --with-man

%files -f %{name}.lang
%doc NEWS README
%{_libdir}/mc
%{_datadir}/mc
%{_sysconfdir}/profile.d/*
%{_sysconfdir}/mc
%{_bindir}/mc
%{_bindir}/mcdiff
%{_bindir}/mcedit
%{_bindir}/mcview
%{_mandir}/man1/*
