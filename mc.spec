# (tpg) we already recommends perl so lets excude any hardcoded modules
%global __requires_exclude ^perl\\(.*\\)|^%{_bindir}/perl

# experimental vfs, gpm and aspell enable
%bcond_without mrb

# avoid dependency on X11 libraries
%bcond_with x11

%bcond_with mc46_style

%define _disable_rebuild_configure 1

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.8.26
Release:	3
License:	GPLv2+
Group:		File tools
Url:		http://www.midnight-commander.org/
Source0:	http://ftp.midnight-commander.org/%{name}-%{version}.tar.xz
Source1:	%{name}.png
Source2:	%{name}.desktop
# Highlight hidden files and dirs with black and
# whitespaces (in mcedit) with bright red like it was in mc 4.6.3 aka Russian fork
Patch0:		mc-4.8.12-old-style-defaults.patch
Patch2:		mc-4.7.2-bash_history.patch
# Revert to pre-4.8.16 behaviour to keep bash history clean
Patch3:		mc-4.8.16-bash_history2.patch
# Needed for GLIB2.0 UNSTABLE! http://midnight-commander.org/ticket/4053
Patch4:		4053.patch
#Patch5:		4053.2.patch
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(slang)
# see http://www.midnight-commander.org/wiki/NEWS-4.8.14
BuildRequires:	glibc-devel  >= 2.14.0
# let's build documentation too. Sflo
BuildRequires:	doxygen

%if %{with x}
BuildRequires:	pkgconfig(x11)
%endif

%if %{with mrb}
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	groff
BuildRequires:	aspell-devel
BuildRequires:	pkgconfig(libssh2) >= 1.2.5
BuildRequires:	pkgconfig(xt)
Recommends:	aspell-en
Recommends:	e2fsprogs
# keep suggested jor full optional.Sflo
# and might include restricted packages.
# ucab extfs
Recommends:	cabextract
# audio extfs
Recommends:	cdparanoia
# iso9660 extfs
Recommends:	cdrkit
# hp48+ extfs
Recommends:	gawk
# spelling corrections
Recommends:	aspell
# CVS support
Recommends:	config(cvs)
# a+ extfs
Recommends:	config(mtools)
# needed by several extfs scripts
Recommends:	perl
# s3+ extfs
# (tpg) do not pull python2
#Recommends:	pythonegg(boto)
#Recommends:	pythonegg(pytz)
# uace extfs
Recommends:	unace
# uarj extfs
Recommends:	unarj
# urar extfs
Recommends:	unrar
# uzip extfs
Recommends:	zip
# support for 7zip archives
Recommends:	p7zip
%endif

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.

%files -f %{name}.lang
%doc doc/FAQ doc/COPYING doc/NEWS doc/README
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcview
%{_bindir}/mcdiff
%{_datadir}/mc/*
%{_libexecdir}/mc/cons.saver
%{_libexecdir}/mc/mc*
%{_libexecdir}/mc/extfs.d/*
%{_libexecdir}/mc/ext.d/*
%{_libexecdir}/mc/fish/*
%{_mandir}/man1/*
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/mc/mc.ext
%config(noreplace) %{_sysconfdir}/mc/*edit*
%config(noreplace) %{_sysconfdir}/mc/mc*.keymap
%config(noreplace) %{_sysconfdir}/mc/mc.menu*
%config(noreplace) %{_sysconfdir}/mc/*.ini
%dir %{_datadir}/mc
%dir %{_sysconfdir}/mc
%dir %{_libexecdir}/mc
%dir %{_libexecdir}/mc/fish
%dir %{_libexecdir}/mc/extfs.d
%dir %{_libexecdir}/mc/ext.d
# Menu entry
%{_datadir}/applications/mc.desktop
%{_iconsdir}/hicolor/*/*/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -q
%if %{with mc46_style}
%patch0 -p1 -b .mc46-style
%endif
%patch2 -p1 -b .bash_history
%patch3 -p1 -b .bash_history2
%patch4	-p1
#patch5	-p1
sed -i 's:|hxx|:|hh|hpp|hxx|:' misc/syntax/Syntax.in

%build
#%%serverbuild
export X11_WWW="www-browser"
export CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE %{optflags} -Wno-strict-aliasing"

autoreconf -fi
%configure \
	--enable-dependency-tracking \
	--without-included-gettext \
	--without-included-slang \
	--with-screen=slang \
	--with-search-engine=glib \
	--enable-nls \
	--enable-charset \
	--enable-largefile \
	--disable-rpath \
	--enable-vfs-mcfs \
	--with-mcfs \
	--enable-extcharset \
	--with-ext2undel \
	--with-mmap \
%if %{with mrb}
	--enable-vfs-smb \
	--enable-vfs-sftp \
	--with-gpm-mouse \
	--enable-aspell \
%endif
%if %{with x}
	--without-x \
%endif
	--libexecdir=%{_libexecdir}

%make_build

%install
%make_install
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
install contrib/{mc.sh,mc.csh} %{buildroot}%{_sysconfdir}/profile.d

# Menu entry:
desktop-file-install %{SOURCE2} \
  --dir=%{buildroot}%{_datadir}/applications
# icons
install -d 755 %{buildroot}%{_iconsdir}/hicolor/scalable
for size in 256x256 128x128 96x96 64x64 48x48 32x32 22x22 16x16 ; do
    install -dm 0755 \
        %{buildroot}%{_iconsdir}/hicolor/$size/apps
    convert -strip -resize $size %{SOURCE1} \
        %{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png
done

# end entry here. Sflo


%find_lang %{name} --with-man
