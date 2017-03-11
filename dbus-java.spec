%{?_javapackages_macros:%_javapackages_macros}

# the package is arch-dependent because scripts contain arch dependent paths
# the debuginfo package will be empty if produced
%global debug_package %{nil}

Name:       dbus-java
Version:    2.7
Release:    23.1
Summary:    Java implementation of the DBus protocol
Group:      Development/Java
License:    AFL or LGPLv2
URL:        http://freedesktop.org/wiki/Software/DBusBindings
#URL2:      http://dbus.freedesktop.org/doc/dbus-java/
Source0:    http://dbus.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

# OSGi manifests
Source1:    %{name}-osgi-MANIFEST.MF

Patch1:     classpath_fix.patch
# fedora specific paths
Patch2:     parallel.patch
# java-7 compatibility patch
# https://bugs.freedesktop.org/show_bug.cgi?id=44791
Patch3:     utf-8-encoding.patch
Patch4:     version-less-jars.patch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  texlive
BuildRequires:  docbook-utils
BuildRequires:  gettext
BuildRequires:  libmatthew-java
BuildRequires:  docbook2x

Requires:   java >= 1:1.6.0
Requires:   javapackages-tools
Requires:   libmatthew-java

%description
D-Bus is a message bus system, a simple way for applications to
talk to one another. In addition to interprocess communication,
D-Bus helps coordinate process lifecycle; it makes it simple and
reliable to code a "single instance" application or daemon, and to
launch applications and daemons on demand when their services are
needed.

This is a complete independent implementation of the D-Bus protocol
in Java. It comprises a library to write programs in Java which
access D-Bus, a tool for generating stubs from D-Bus introspection
data and a simple daemon. Being written in Java it works on both
Windows and Linux (and other Unix-like systems).

When using a TCP transport it is entirely Java-based; when using
Unix-sockets it requires a small JNI library to use Unix-Sockets.


%package javadoc
Summary:    Javadocs for %{name}
Group:      Development/Java
Requires:   jpackage-utils


%description javadoc
Javadocs for %{name}


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -i "s|!doctype|!DOCTYPE|g" *.sgml
sed -i 's|<!DOCTYPE refentry PUBLIC "-//OASIS//DTD DocBook V4.1//EN"|<!DOCTYPE refentry PUBLIC "-//OASIS//DTD DocBook V4.1//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"|g' *.sgml

%build
# no configure file
%make \
    DOCBOOKTOMAN="docbook2x-man"\
    -j1 \
    JARPREFIX=%{_javadir}/%{name} \
    BINPREFIX=%{_bindir} \
    MANPREFIX=%{_mandir}/man1 \
    DOCPREFIX=%{_defaultdocdir}/%{name} \
    JAVADOCPREFIX=%{_javadocdir}/%{name} \
    JAVAUNIXLIBDIR=%{_libdir}/libmatthew-java \
    JAVAUNIXJARDIR=%{_jnidir} \
    JAVADOC="javadoc -Xdoclint:none"

# Inject OSGi manifests
jar umf %{SOURCE1} libdbus-java-%{version}.jar

%check
make check \
    JARPREFIX=%{_javadir}/%{name} \
    BINPREFIX=%{_bindir} \
    MANPREFIX=%{_mandir}/man1 \
    DOCPREFIX=%{_defaultdocdir}/%{name} \
    JAVADOCPREFIX=%{_javadocdir}/%{name} \
    JAVAUNIXLIBDIR=%{_libdir}/libmatthew-java \
    JAVAUNIXJARDIR=%{_jnidir} \
    JAVADOC="javadoc -Xdoclint:none"


%install
%makeinstall_std \
    DESTDIR=$RPM_BUILD_ROOT \
    JARPREFIX=%{_javadir}/%{name} \
    BINPREFIX=%{_bindir} \
    MANPREFIX=%{_mandir}/man1 \
    DOCPREFIX=%{_defaultdocdir}/%{name} \
    JAVADOCPREFIX=%{_javadocdir}/%{name} \
    JAVAUNIXLIBDIR=%{_libdir}}/libmatthew-java \
    JAVAUNIXJARDIR=%{_jnidir} \
    JAVADOC="javadoc -Xdoclint:none"

%files
%{_javadir}/%{name}
%{_bindir}/CreateInterface
%{_bindir}/DBusCall
%{_bindir}/DBusDaemon
%{_bindir}/DBusViewer
%{_bindir}/ListDBus
#%doc %{_defaultdocdir}/%{name}
%doc %{_mandir}/man1/CreateInterface.1.gz
%doc %{_mandir}/man1/DBusCall.1.gz
%doc %{_mandir}/man1/DBusDaemon.1.gz
%doc %{_mandir}/man1/DBusViewer.1.gz
%doc %{_mandir}/man1/ListDBus.1.gz
%doc AUTHORS INSTALL README
%doc COPYING

%files javadoc
%{_javadocdir}/%{name}
%doc COPYING


%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 31 2015 Omair Majid <omajid@redhat.com> 2.7-21
- Use %%global instead of %%define
- Use %%license instead of %%doc for license files

* Mon Jun 22 2015 Omair Majid <omajid@redhat.com> 2.7-20
- Require javapackages-tools, not jpackage-utils

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 2.7-19
- Fix FTBFS - disable strict doclint.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 18 2013 Omair Majid <omajid@redhat.com> - 2.7-15
- Install only version-less jars

* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 2.7-14
- Fixed paths to jni jars

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 6 2013 Omair Majid <omajid@redhat.com> -2.7.12
- Do not produce an empty debuginfo package
- Resolves bug 917797

* Fri Mar 1 2013 Omair Majid <omajid@redhat.com> - 2.7-11
- Fix build by adding various latex dependencies
- Make package arch-dependent: scripts contain arch-dependent path

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.7-7
- Adapt for building/running with openjdk 7.
- Remove not needed parts.

* Sun Feb 13 2011 Mat Booth <fedora@matbooth.co.uk> 2.7-6
- Inject OSGi manifests into jars so that they may be used in OSGi apps such
  as Eclipse plug-ins.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 8 2010 Omair Majid <omajid@redhat.com> 2.7-4
- Add missing docs to main package and license to javadoc subpackage

* Fri Jan 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-3
- Add docbook2X dependency.

* Fri Jan 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-2
- Fix manpages generation.

* Wed Jan 13 2010 Alexander Kurtakov <akurtako@redhat.com> 2.7-1
- Update to upstream 2.7.
- Drop gcj_support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Omair Majid <omajid@redhat.com> - 2.5.1-1
- update to 2.5.1
- Added patches from François Kooman <fkooman@tuxed.net>
- Added docs.patch (already upstream). Replaces docbook.patch and 
  man_fixes.patch
- Add missing TestSignalInterface2 interface (already upstream)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 7 2008 Omair Majid <omajid@redhat.com> - 2.5-3
- Added a patch to fix the htlatex environment
- added -j1 to make to fix the race condition in makefile

* Mon Jun 30 2008 Omair Majid <omajid@redhat.com> - 2.5-2
- fixed incoherent name warning from rpmlint
- fixed wrapper script paths
- added check section

* Wed Jun 25 2008 Omair Majid <omajid@redhat.com> - 2.5-1
- Initial build
