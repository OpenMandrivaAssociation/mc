# avoid dependency on X11 libraries
%define without_x       1

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.6.1
Release:	%mkrel 6
License:	GPL
Group:		File tools
URL:		http://www.ibiblio.org/mc/
Source0:	ftp://ftp.gnome.org:/pub/GNOME/stable/sources/mc/%{name}-%{version}.tar.bz2
# Changelogs for Advanced Midnight Commander patches
Source1:	http://www1.mplayerhq.hu/~arpi/amc/amc-1.txt
Source2:	http://www1.mplayerhq.hu/~arpi/amc/amc-2.txt
#(dam's)
Patch23:	mc-4.6.0-toolbar-po-mdk.path
# (tv) add runlevel to initscript
Patch31:	mc-4.6.0-init.patch
# (fc) fix xpdf outputing garbage on stdout (bug #4094)
Patch0:		mc-4.6.0-xpdf.patch
# remove copyright tag, and s/serial/epoch tag in rpm vfs
Patch1:		mc-4.6.1-rpm_obsolete_tags.patch
# (mpol) 4.6.0-9mdk
Patch6:		mc-4.6.0-ptsname.patch
# (mpol) 4.6.0-9mdk utf8 patches from fedora/suse
Patch7:		mc-4.6.1-utf8.patch
Patch8:		mc-4.6.1-bourne-compliancy.patch
Patch9:		mc-4.6.1-decent_defaults.diff
# PLD patches P100 - P113
Patch100:	mc-spec-syntax.patch
Patch101:	mc-urar.patch
Patch102:	mc-srpm.patch
# Advanced Midnight Commander patches
#changed from:	http://www1.mplayerhq.hu/~arpi/amc/amc-1.diff
Patch103:	amc-1.diff
#changed from:	http://www1.mplayerhq.hu/~arpi/amc/amc-2.diff
Patch104:	amc-2.diff
Patch105:	mc-mc.ext.patch
Patch106:	mc-mo.patch
# at now syntax highligthing for PLD-update-TODO and CVSROOT/users
Patch107:	mc-pld-developerfriendly.patch
# http://www.suse.de/~nadvornik/mc.html
Patch108:	mc-64bit.patch
Patch109:	mc-fish-upload.patch
Patch110:	mc-nolibs.patch
Patch111:	mc-ftpcrash.patch
Patch112:	mc-symcrash.patch
Patch113:	mc-userhost.patch
Patch114:	mc-4.6.1.lzma.patch
Requires:	groff
Requires:	slang > 1.4.9-5mdk
BuildRequires:	libext2fs-devel
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel > 1.4.9-5mdk
BuildRequires:	glib2-devel
BuildRequires:  autoconf2.5
%if %without_x
%else
BuildRequires:	XFree86-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.  :-)

%prep

%setup -q -n %{name}-%{version}

%patch0 -p1 -b .xpdf
%patch1 -p1 -b .rpm_obsolete_tags
%patch23 -p1 -b .toolbarpo
%patch31 -p1 -b .initlevel
# fixme: disabled P6
#%%patch6 -p1 -b .ptsname
%patch7 -p1 -b .utf8
%patch8 -p1 -b .bourne_compliancy
%patch9 -p0 -b .decent_defaults

# PLD patches
%patch100 -p1
%patch101 -p1
cp -f vfs/extfs/{rpm,srpm}
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1 -b .lzma

sed -i 's:|hxx|:|hh|hpp|hxx|:' syntax/Syntax

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

X11_WWW="www-browser" %serverbuild
# libcom_err of e2fsprogs and krb5 conflict. Watch this hack. -- Geoff.
# <hack>
mkdir -p %{_lib}
ln -sf /%{_lib}/libcom_err.so.2 %{_lib}/libcom_err.so
export LDFLAGS="-L`pwd`/%{_lib}"
# </hack>

%configure2_5x \
    --with-debug \
    --without-included-gettext \
    --without-included-slang \
    --with-screen=slang \
    --enable-nls \
    --enable-charset \
    --enable-largefile \
%if %without_x
    --without-x
%endif

# don't use make macro, mc doesn't support parallel compilation
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,profile.d,X11/wmconfig} $RPM_BUILD_ROOT%{_initrddir}

#fix mc-wrapper.sh
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall

install lib/{mc.sh,mc.csh} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root)
%doc FAQ COPYING NEWS README
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcmfmt
%{_bindir}/mcview
%dir %{_libdir}/mc/
%{_libdir}/mc/cons.saver
%{_datadir}/mc/cedit.menu
%{_datadir}/mc/edit.indent.rc
%{_datadir}/mc/edit.spell.rc
%{_datadir}/mc/mc.ext
%{_datadir}/mc/mc.hint
%{_datadir}/mc/mc.hint.*
%{_datadir}/mc/mc.hlp
%{_datadir}/mc/mc.hlp.*
%{_datadir}/mc/mc.lib
%{_datadir}/mc/mc.menu
%{_datadir}/mc/mc.menu.*
%{_datadir}/mc/mc.charsets
%{_datadir}/mc/extfs/*
%{_mandir}/man1/*
%dir %{_datadir}/mc
%dir %{_datadir}/mc/bin
%{_datadir}/mc/bin/*
%{_datadir}/mc/syntax/
#%{_datadir}/mc/term/
%{_sysconfdir}/profile.d/*


