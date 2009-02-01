# avoid dependency on X11 libraries
%define without_x       1

%define rel	1
%define	cvs	0
# cvs -z3 -d:pserver:anoncvs@cvs.savannah.gnu.org:/cvsroot/mc co mc

%if %cvs
%define release		%mkrel 3.%{cvs}.%{rel}
%define distname	%{name}-%{cvs}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.6.2
Release:	%{release}
License:	GPLv2+
Group:		File tools
URL:		http://www.midnight-commander.org/
Source0:	http://www.midnight-commander.org/downloads/%{distname}

# ** Mandriva patches: 0 - 99 **

# remove copyright tag, and s/serial/epoch tag in rpm vfs
Patch1:		mc-4.6.2-rpm_obsolete_tags.patch
Patch2:		mc-4.6.0-toolbar-po-mdk.path
# (tv) add runlevel to initscript
Patch3:		mc-4.6.0-init.patch
#Patch4:	mc-4.6.0-ptsname.patch
Patch5:		mc-4.6.1-bourne-compliancy.patch
Patch6:		mc-4.6.1-decent_defaults.diff
# from https://savannah.gnu.org/bugs/?16303: improves the 7zip handler
# slightly. Modified not to test for '7z', as we don't package it, 
# only '7za' - AdamW 2007/07
Patch7:		u7z.patch
Patch8:		mc-4.6.1.lzma.patch
Patch9:		mc-4.6.1-xdg.patch
Patch10:	mc-4.6.2-shortcut.patch

# ** Fedora patchset: 100 - 199 **

# UTF-8 patches, rediffed by AdamW for 20071018 snapshot
Patch100:	mc-utf8.patch
Patch101:	mc-utf8-8bit-hex.patch
# Hostname
Patch102:	mc-userhost.patch
Patch103:	mc-utf8-look-and-feel.patch
# IPv6 support for FTPFS
Patch104:	mc-ipv6.patch
# refresh contents of terminal when resized during time expensive I/O
# operations
Patch105:	mc-refresh.patch
Patch106:	mc-64bit.patch
# correctly concatenate directory and file in concat_dir_and_file()
Patch107:	mc-concat.patch
# display free space correctly for multiple filesystems
Patch108:	mc-showfree.patch
# Update panel contents to avoid actions on deleted files
Patch109:	mc-delcheck.patch
# allow exit command even on non-local filesystems (#202440)
Patch110:	mc-exit.patch
Patch111:	mc-newlinedir.patch
# attempt to fcntl() descriptors appropriately so that subshell
#  doesn't leave them open while execve()ing commands
Patch112:	mc-cloexec.patch
# fix displaying of prompt in subshell
Patch113:	mc-prompt.patch

# ** PLD patchset: 200 - 299 **

Patch200:	mc-spec-syntax.patch
Patch201:	mc-urar.patch
Patch202:	mc-srpm.patch
Patch203:	mc-mc.ext.patch
Patch204:	mc-localenames.patch
Patch205:	mc-nolibs.patch
Patch206:	mc-vhdl-syntax.patch

# From OpenSUSE: fix display of nlinks column in UTF-8 locales
# (#34207, SUSE #194715) - AdamW 2008/01
Patch300:	mc-utf8-nlink.patch

Requires:	groff
BuildRequires:	libext2fs-devel
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel
BuildRequires:	glib2-devel
BuildRequires:  autoconf
%if %without_x
%else
BuildRequires:	X11-devel
%endif
%if %cvs
BuildRequires:	gettext-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.

%prep
%setup -q -n %{dirname}

%patch1 -p1 -b .rpm_obsolete_tags
%patch2 -p1 -b .toolbarpo
%patch3 -p1 -b .initlevel
# fixme: disabled P4
#%%patch4 -p1 -b .ptsname
%patch5 -p1 -b .bourne_compliancy
%patch6 -p0 -b .decent_defaults
%patch7 -p0 -b .u7z
%patch8 -p1 -b .lzma
%patch9 -p0 -b .xdg
%patch10 -p1 -b .shortcut

%patch100 -p1
%patch101 -p1
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

%patch200 -p1
%patch201 -p0
cp -f vfs/extfs/{rpm,srpm}
%patch202 -p1
%patch203 -p1
%patch204 -p0
%patch205 -p1
%patch206 -p1

%patch300 -p1 -b .nlink

sed -i 's:|hxx|:|hh|hpp|hxx|:' syntax/Syntax

mv -f po/{no,nb}.po

%build

# Convert translated files to UTF-8: bug #31578 - AdamW 2007/06

pushd doc
# italian is already unicode, leave it out.
for i in es hu pl ru sr; do pushd $i; \
# this is ugly, but assume same encoding as .po file for each language.
iconv --from-code=`grep charset= ../../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 mc.1.in > mc.1.in.new; \
iconv --from-code=`grep charset= ../../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 xnc.hlp > xnc.hlp.new; \
mv -f mc.1.in.new mc.1.in; mv -f xnc.hlp.new xnc.hlp; popd; done
popd

pushd lib
# rename zh to zh_TW, which is what it really is (I think)
mv mc.hint.zh mc.hint.zh_TW
perl -pi -e 's,mc.hint.zh,mc.hint.zh_TW,g' Makefile.am
# hardcode the list as we need to leave italian out and it just gets ugly doing it 'smartly'...
for i in cs es hu nl pl ru sr uk zh_TW; \
# this is ugly, but assume same encoding as .po file for each language.
do iconv --from-code=`grep charset= ../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 mc.hint.$i > mc.hint.$i.new; \
mv -f mc.hint.$i.new mc.hint.$i; done
popd

pushd po
# remove the original .mo files
rm -f *.gmo
# find stuff that's not Unicode already
for i in `file *.po | grep -v Unicode | cut -d: -f1`; \
# convert it: the grep, cut, head, tr grabs the source encoding from the .po file header, there's no other way to find it
do iconv --from-code=`grep charset= $i | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 $i > $i.new; \
# change the header to say UTF-8
mv -f $i.new $i; perl -pi -e 's,charset=.*$,charset=UTF-8\\n",g' $i; done
# regenerate the .mo files
for i in `ls *.po | cut -d. -f1`; do /usr/bin/msgfmt -c --statistics -o $i.gmo $i.po; done
popd

# update the menu entry for directory hotlist to match change in shortcut.patch
sed -i -e 's,C-\\\\,C-\\\\ or C-l,g' src/main.c po/*.po

%if %cvs
./autogen.sh
%else
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%endif

X11_WWW="www-browser" %serverbuild

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
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/{pam.d,profile.d,X11/wmconfig} %{buildroot}%{_initrddir}

#fix mc-wrapper.sh
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall

install -m 644 lib/mc.sh %{buildroot}%{_sysconfdir}/profile.d/20mc.sh
install -m 644 lib/mc.csh %{buildroot}%{_sysconfdir}/profile.d/20mc.csh

%{find_lang} %{name}

%clean
rm -rf %{buildroot}


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
