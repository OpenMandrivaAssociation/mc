# avoid dependency on X11 libraries
%define without_x       1

%define Werror_cflags %nil
%define rel	1
%define	prel	pre2
# cvs -z3 -d:pserver:anoncvs@cvs.savannah.gnu.org:/cvsroot/mc co mc

%if %prel
%define release		%mkrel -c %{prel} 2
%define distname	%{name}-%{version}-%{prel}.tar.bz2
%define dirname		%{name}-%{version}-%{prel}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif


Summary:	A user-friendly file manager and visual shell
Name:		mc
Version:	4.7.0
Release:	%{release}
License:	GPLv2+
Group:		File tools
URL:		http://www.midnight-commander.org/
Source0:	http://www.midnight-commander.org/downloads/%{distname}
# using correct symlinks for automake 1.11
Source1:	mc-4.6.2-automake1.11.tar.bz2

# ** Mandriva patches: 0 - 99 **

# (tv) add runlevel to initscript
Patch0:		mc-4.7.0-pre2-xz-support.patch
Patch3:		mc-4.6.0-init.patch
#Patch4:	mc-4.6.0-ptsname.patch
Patch6:		mc-4.7.0-pre2-decent_defaults.patch
Patch9:		mc-4.6.2-xdg.patch
Patch10:	mc-4.6.2-shortcut.patch
Patch11:	mc-4.6.2-do-not-mark-tabs.patch
Patch12:	mc-4.7.0-pre2-missing-mhl-header.patch
Patch13:	mc-4.6.2-pl-po.patch

# ** Fedora patchset: 100 - 199 **

# Hostname
Patch102:	mc-4.6.2-userhost.patch
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

Requires:	groff
BuildRequires:	libext2fs-devel
BuildRequires:	libgpm-devel >= 0.18
BuildRequires:	pam-devel
BuildRequires:	slang-devel
Buildrequires:	glib2-devel
BuildRequires:	pcre-devel
BuildRequires:  autoconf
BuildRequires:	bison
%if %without_x
%else
BuildRequires:	X11-devel
%endif
%if %prel
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
tar xjf %SOURCE1

%patch0 -p1 -b .xz
#%patch3 -p1 -b .initlevel rediff?
# fixme: disabled P4
#%%patch4 -p1 -b .ptsname
%patch6 -p1 -b .decent_defaults
#%patch9 -p1 -b .xdg rediff?
%patch10 -p1 -b .shortcut
%patch11 -p1 -b .tabs
%patch12 -p1 -b .mhl
#%patch13 -p1 -b .pl rediff?

#%patch102 -p1 rediff?
%patch105 -p1
#%patch106 -p1 rediff?
#%patch107 -p1 rediff?
#%patch108 -p1 rediff?
#%patch109 -p1 rediff?
#%patch110 -p1 rediff?
#%patch111 -p1 rediff?
#%patch113 -p1 rediff?

cp -f vfs/extfs/{rpm,srpm}
#%patch202 -p1 rediff?
#%patch203 -p1 rediff?
#%patch204 -p0 rediff?
#%patch205 -p1 rediff?

#%patch300 -p1 -b .homedir rediff?

sed -i 's:|hxx|:|hh|hpp|hxx|:' syntax/Syntax

#mv -f po/{no,nb}.po

%build

# Convert translated files to UTF-8: bug #31578 - AdamW 2007/06

#pushd doc
# italian and spanish are already unicode, leave it out.
#for i in hu pl ru sr; do pushd $i; \
# this is ugly, but assume same encoding as .po file for each language.
#iconv --from-code=`grep charset= ../../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 mc.1.in > mc.1.in.new; \
#iconv --from-code=`grep charset= ../../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 xnc.hlp > xnc.hlp.new; \
#mv -f mc.1.in.new mc.1.in; mv -f xnc.hlp.new xnc.hlp; popd; done
#popd

#pushd lib
# rename zh to zh_TW, which is what it really is (I think)
#mv mc.hint.zh mc.hint.zh_TW
#perl -pi -e 's,mc.hint.zh,mc.hint.zh_TW,g' Makefile.am
# hardcode the list as we need to leave es, it out and it just gets ugly doing it 'smartly'...
#for i in cs hu nl pl ru sr uk zh_TW
# this is ugly, but assume same encoding as .po file for each language.
#do iconv --from-code=`grep charset= ../po/$i.po | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 mc.hint.$i > mc.hint.$i.new; \
#mv -f mc.hint.$i.new mc.hint.$i; done
#popd

#pushd po
# remove the original .mo files
#rm -f *.gmo
# find stuff that's not Unicode already
#for i in `file *.po | grep -v Unicode | cut -d: -f1`; \
# convert it: the grep, cut, head, tr grabs the source encoding from the .po file header, there's no other way to find it
#do iconv --from-code=`grep charset= $i | cut -c36- | head -c-4 | tr "[:lower:]" "[:upper:]"` --to-code=UTF-8 $i > $i.new; \
# change the header to say UTF-8
#mv -f $i.new $i; perl -pi -e 's,charset=.*$,charset=UTF-8\\n",g' $i; done
# regenerate the .mo files
#for i in `ls *.po | cut -d. -f1`; do /usr/bin/msgfmt -c --statistics -o $i.gmo $i.po; done
#popd

# update the menu entry for directory hotlist to match change in shortcut.patch
#sed -i -e 's,C-\\\\,C-\\\\ or C-l,g' src/main.c po/*.po

%if %prel
#./autogen.sh
%else
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%endif
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
%if %without_x
    --without-x
%endif

%make

%install
rm -rf %{buildroot}

#fix mc-wrapper.sh
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall_std

install -m644 contrib/mc.sh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.sh
install -m644 contrib/mc.csh -D %{buildroot}%{_sysconfdir}/profile.d/20mc.csh

%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcmfmt
%{_bindir}/mcview
%{_sysconfdir}/mc
%{_libdir}/mc/mc*.*sh
%dir %{_libdir}/mc/
%{_libdir}/mc/cons.saver
%{_datadir}/mc/mc.hint
%{_datadir}/mc/mc.hint.*
%{_datadir}/mc/mc.hlp
%{_datadir}/mc/mc.hlp.*
%{_datadir}/mc/mc.menu.*
%{_datadir}/mc/extfs/*
%{_mandir}/*/man1/*
%{_mandir}/man1/*
%dir %{_datadir}/mc
%{_datadir}/mc/syntax/
%{_sysconfdir}/profile.d/*
