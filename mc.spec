# avoid dependency on X11 libraries
%define without_x       1

%define Werror_cflags %nil

Name:		mc
Version:	4.8.3
Release:	%mkrel 1
Summary:	A user-friendly file manager and visual shell
License:	GPLv2+
Group:		File tools
URL:		http://www.midnight-commander.org/
Source0:	http://www.midnight-commander.org/downloads/%{name}-%{version}.tar.xz

# ** Mandriva patches: 0 - 99 **

# (tv) add runlevel to initscript
Patch3:		mc-4.6.0-init.patch
Patch6:		mc-4.7.0-pre2-decent_defaults.patch
Patch9:		mc-4.8.0-xdg.patch
Patch10:	mc-4.6.2-shortcut.patch
Patch11:	mc-4.7.0.2-do-not-mark-tabs.patch
Patch13:	mc-4.6.2-pl-po.patch
Patch14:	mc-4.7.2-bash_history.patch

# ** Fedora patchset: 100 - 199 **

# Hostname
Patch102:	mc-4.6.2-userhost.patch
# refresh contents of terminal when resized during time expensive I/O
# operations
#Patch105:	mc-refresh.patch
Patch106:	mc-64bit.patch
# correctly concatenate directory and file in concat_dir_and_file()
Patch107:	mc-concat.patch
# display free space correctly for multiple filesystems
Patch108:	mc-showfree.patch
# Update panel contents to avoid actions on deleted files
Patch109:	mc-delcheck.patch
# allow exit command even on non-local filesystems (#202440)
Patch110:	mc-exit.patch
Patch111:	mc-4.6.2-newlinedir.patch
# fix displaying of prompt in subshell
Patch113:	mc-prompt.patch

# ** PLD patchset: 200 - 299 **

Patch202:	mc-srpm.patch
Patch203:	mc-mc.ext.patch
Patch204:	mc-localenames.patch
Patch205:	mc-nolibs.patch

# ** Other patches: 300 - 399 **
# based on upstream commit d0beb4cfec
Patch300:	mc-4.6.2-create-homedir.patch
Patch301:	mc-4.7.0-pre4-use_okular_for_pdf_files.diff

BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel
Buildrequires:	glib2-devel
BuildRequires:	pcre-devel
BuildRequires:	autoconf
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
%setup -q -n %{name}-%{version}

#patch3 -p1 -b .initlevel rediff?
%patch6 -p0 -b .decent_defaults
%patch9 -p1 -b .xdg
#patch10 -p1 -b .shortcut rediff?
%patch11 -p0 -b .tabs
#patch13 -p1 -b .pl rediff?
%patch14 -p1

#%patch102 -p1 rediff?
#patch105 -p0 -b .refresh
#%patch106 -p1 rediff?
#%patch107 -p1 rediff?
#%patch108 -p1 rediff?
#%patch109 -p1 rediff?
#%patch110 -p1 rediff?
#%patch111 -p1 rediff?
#%patch113 -p1 rediff?

#cp -f lib/vfs/mc-vfs/extfs/{rpm,srpm}
#%patch202 -p1 rediff?
#%patch203 -p1 rediff?
#%patch204 -p0 rediff?
#%patch205 -p1 rediff?

#%patch300 -p1 -b .homedir rediff?
#%patch301 -p0 -b .use_okular_for_pdf_files patch9 does the job

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
%__rm -rf %{buildroot}

#fix mc-wrapper.sh
%__perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall_std

%__install -m644 contrib/mc.sh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.sh
%__install -m644 contrib/mc.csh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.csh

%find_lang %{name} --with-man

%clean
%__rm -rf %{buildroot}

%files -f %{name}.lang
%doc NEWS README
%dir %{_libdir}/mc
%dir %{_libdir}/mc/extfs.d
%dir %{_libdir}/mc/fish
%dir %{_datadir}/mc
%dir %{_datadir}/mc/skins
%dir %{_datadir}/mc/syntax
%dir %{_datadir}/mc/hints
%dir %{_datadir}/mc/help
%dir %{_datadir}/mc/examples
%{_sysconfdir}/profile.d/*
%{_sysconfdir}/mc
%{_bindir}/mc
%{_bindir}/mcdiff
%{_bindir}/mcedit
%{_bindir}/mcview
%{_libdir}/mc/cons.saver
%{_libdir}/mc/extfs.d/*
%{_libdir}/mc/fish/*
%{_libdir}/mc/mc*.*sh
%{_datadir}/mc/help/*
%{_datadir}/mc/hints/*
%{_datadir}/mc/mc.charsets
%{_datadir}/mc/mc.lib
%{_datadir}/mc/skins/*
%{_datadir}/mc/syntax/*
%{_mandir}/man1/*
%{_datadir}/mc/examples/macros.d/*
