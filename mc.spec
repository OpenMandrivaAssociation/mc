# avoid dependency on X11 libraries
%define without_x       1

Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.6.1
Release:	%mkrel 17
License:	GPLv2+
Group:		File tools
URL:		http://www.ibiblio.org/mc/
Source0:	ftp://ftp.gnome.org:/pub/GNOME/stable/sources/mc/%{name}-%{version}.tar.bz2
# Changelogs for Advanced Midnight Commander patches
Source1:	http://www1.mplayerhq.hu/~arpi/amc/amc-1.txt
Source2:	http://www1.mplayerhq.hu/~arpi/amc/amc-2.txt
# From upstream CVS: adds a 7Zip VFS handler -AdamW 2007/07
Source3:	u7z
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
# from upstream
Patch10:	mc-bash32.diff
# from https://savannah.gnu.org/bugs/?16303: improves the 7zip handler
# slightly modified not to test for '7z', as we don't package it, only
# '7za' - AdamW 2007/07
Patch11:	u7z.patch
# from https://savannah.gnu.org/bugs/?13953: fixes a bug that left temp
# files lying around. see also MDV bug #15687. rediffed - AdamW 2007/09
Patch12:	mc-4.6.1-tempfiles.patch
# from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=349390 and
# https://savannah.gnu.org/bugs/?15524: fixes a bug which made ssh
# file transfers larger than 2GB fail (MDV bug #34063)
Patch13:	mc-4.6.1-2gb.patch
# PLD patches P100 - P114
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
# This is a kinda mash-up of the SUSE and PLD slang2 patches. It
# works, don't knock it. -AdamW, 2007/06
Patch114:	mc-slang2.patch
# Patches 200 on must be applied after PLD patches; if you have
# a new patch that can be applied before the PLD patches, don't put
# it here
Patch200:	mc-4.6.1.lzma.patch
Patch201:	mc-4.6.1-xdg.patch
# from upstream CVS: changes to accommodate the 7zip VFS handler
Patch202:	mc-4.6.1-7zip.patch
Requires:	groff
BuildRequires:	libext2fs-devel
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel
BuildRequires:	glib2-devel
BuildRequires:  autoconf
%if %without_x
%else
BuildRequires:	XFree86-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  Its coolest feature is the ability to ftp, view tar, zip
files, and poke into RPMs for specific files.

%prep

%setup -q -n %{name}-%{version}

# Add u7z VFS handler - AdamW 2007/07
install -m755 %{SOURCE3} vfs/extfs/u7z

%patch0 -p1 -b .xpdf
%patch1 -p1 -b .rpm_obsolete_tags
%patch23 -p1 -b .toolbarpo
%patch31 -p1 -b .initlevel
# fixme: disabled P6
#%%patch6 -p1 -b .ptsname
%patch7 -p1 -b .utf8
%patch8 -p1 -b .bourne_compliancy
%patch9 -p0 -b .decent_defaults
%patch10 -p0 -b .bash32
%patch11 -p1 -b .u7z
%patch12 -p1 -b .tempfiles
%patch13 -p1 -b .2gb

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
%patch114 -p0
 
%patch200 -p1 -b .lzma
%patch201 -p1 -b .xdg
%patch202 -p1 -b .7zip

sed -i 's:|hxx|:|hh|hpp|hxx|:' syntax/Syntax

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

# I don't know why install -m755 above doesn't work, but whatever.
# - AdamW 2007/07

chmod ugo+x $RPM_BUILD_ROOT%{_datadir}/mc/extfs/u7z

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
