# avoid dependency on X11 libraries
%define without_x 1
%define mc46_style 0

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.8.9
Release:	1
License:	GPLv2+
Group:		File tools
Url:		http://www.midnight-commander.org/
Source0:	http://ftp.midnight-commander.org/%{name}-%{version}.tar.xz
# Highlight hidden files and dirs with black and
# whitespaces (in mcedit) with bright red like it was in mc 4.6.3 aka Russian fork
Patch0:		mc-4.8.8-old-style-defaults.patch
Patch1:		mc-4.7.0.2-do-not-mark-tabs.patch
Patch2:		mc-4.7.0-pre2-decent_defaults.patch
Patch3:		mc-4.7.2-bash_history.patch
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(slang)
%if !%{without_x}
BuildRequires:	X11-devel
%endif
Requires:	groff

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.

%prep
%setup -q
%if %{mc46_style}
%patch0 -p1 -b .mc46-style
%else
%patch1 -p0 -b .tabs
%endif
%patch2 -p0 -b .decent_defaults
%patch3 -p1 -b .bash_history

sed -i 's:|hxx|:|hh|hpp|hxx|:' misc/syntax/Syntax.in

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
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall_std

install -m644 contrib/mc.sh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.sh
install -m644 contrib/mc.csh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.csh

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
