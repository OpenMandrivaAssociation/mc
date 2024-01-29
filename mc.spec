# (tpg) optimizxe it a bit
%global optflags %{optflags} -Oz --rtlib=compiler-rt

# (tpg) we already recommends perl so lets excude any hardcoded modules
%global __requires_exclude ^perl\\(.*\\)|^%{_bindir}/perl

%define _disable_rebuild_configure 1

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.8.31
Release:	1
License:	GPLv2+
Group:		File tools
Url:		https://www.midnight-commander.org/
Source0:	https://ftp.midnight-commander.org/%{name}-%{version}.tar.xz
Source1:	%{name}.png
Source2:	%{name}.desktop
Patch2:		mc-4.7.2-bash_history.patch
# Revert to pre-4.8.16 behaviour to keep bash history clean
Patch3:		mc-4.8.16-bash_history2.patch
# Needed for GLIB2.0 UNSTABLE! http://midnight-commander.org/ticket/4053
Patch4:		4053.patch
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
Recommends:	mkisofs
Recommends:	xorriso
# hp48+ extfs
Recommends:	gawk
# spelling corrections
Recommends:	aspell
# a+ extfs
Recommends:	config(mtools)
# needed by several extfs scripts
Recommends:	perl
# s3+ extfs
# uace extfs
Recommends:	unace
# uarj extfs
Recommends:	unarj
# urar extfs
Recommends:	unrar
# uzip extfs
Recommends:	zip
# support for 7zip archives
Recommends:	7zip

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
%doc %{_mandir}/man1/*
%{_sysconfdir}/profile.d/*
#config(noreplace) %{_sysconfdir}/mc/mc.ext
%config(noreplace) %{_sysconfdir}/mc/*edit*
%config(noreplace) %{_sysconfdir}/mc/mc*.keymap
%config(noreplace) %{_sysconfdir}/mc/mc.menu*
%config(noreplace) %{_sysconfdir}/mc/*.ini
%dir %{_datadir}/mc
%dir %{_sysconfdir}/mc
%dir %{_libexecdir}/mc
%dir %{_libexecdir}/mc/extfs.d
%dir %{_libexecdir}/mc/ext.d
# Menu entry
%{_datadir}/applications/mc.desktop
%{_iconsdir}/hicolor/*/*/%{name}.png

#----------------------------------------------------------------------------

%prep
%autosetup -p1

sed -i 's:|hxx|:|hh|hpp|hxx|:' misc/syntax/Syntax.in

%build
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
	--enable-vfs-smb \
	--enable-vfs-sftp \
	--with-gpm-mouse \
	--enable-aspell \
	--without-x \
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
