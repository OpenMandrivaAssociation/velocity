# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


%define section free


Name:           velocity
Version:        1.7
Release:        4
Epoch:          0
Summary:        Java-based template engine
License:        Apache Software License
Source0:        http://www.apache.org/dist/%{name}/engine/%{version}/%{name}-%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/org/apache/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Patch0:         0001-Remove-avalon-logkit.patch
Patch2:         0003-Use-system-jars.patch
Patch3:         0004-JDBC-41-compat.patch
Group:          Development/Libraries/Java
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-logging
Requires:       jakarta-commons-lang
Requires:       tomcat6-servlet-2.5-api
Requires:       oro
Requires:       werken-xpath
Requires:       junit
Requires:       hsqldb
Requires:       jdom
Requires:       bcel
Requires:       log4j
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildRequires:  werken-xpath
BuildRequires:  ant
BuildRequires:  antlr
BuildRequires:	antlr-java
BuildRequires:  junit
BuildRequires:  ant-junit
BuildRequires:  hsqldb
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-commons-lang
BuildRequires:  tomcat6-servlet-2.5-api
BuildRequires:  oro
BuildRequires:  jdom
BuildRequires:  bcel
BuildRequires:  log4j
BuildRequires:  jpackage-utils
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  xerces-j2

URL:            http://velocity.apache.org/
Group:          Development/Java
# Use servletapi5 instead of servletapi5
Requires:       servlet25
Requires:       werken.xpath

# It fails one of the arithmetic test cases with gcj
BuildRequires:  java-devel >= 1.6.0
BuildRequires:	java-1.7.0-openjdk-devel
BuildArch:      noarch

%description
Velocity is a Java-based template engine. It permits anyone to use the
simple yet powerful template language to reference objects defined in
Java code.
When Velocity is used for web development, Web designers can work in
parallel with Java programmers to develop web sites according to the
Model-View-Controller (MVC) model, meaning that web page designers can
focus solely on creating a site that looks good, and programmers can
focus solely on writing top-notch code. Velocity separates Java code
from the web pages, making the web site more maintainable over the long
run and providing a viable alternative to Java Server Pages (JSPs) or
PHP.
Velocity's capabilities reach well beyond the realm of web sites; for
example, it can generate SQL and PostScript and XML (see Anakia for more
information on XML transformations) from templates. It can be used
either as a standalone utility for generating source code and reports,
or as an integrated component of other systems. Velocity also provides
template services for the Turbine web application framework.
Velocity+Turbine provides a template service that will allow web
applications to be developed according to a true MVC model.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
Documentation for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}


%description    demo
Demonstrations and samples for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}

# remove bundled libs/classes (except those used for testing)
find . -name '*.jar' -o -name '*.class' -not -path '*test*' -print -delete

# Remove dependency on avalon-logkit
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogChute.java
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogSystem.java
rm -f src/java/org/apache/velocity/runtime/log/VelocityFormatter.java

# need porting to new servlet API. We would just add a lot of empty functions
rm  src/test/org/apache/velocity/test/VelocityServletTestCase.java

cp %{SOURCE1} ./pom.xml

# remove rest of avalon logkit refences
%patch0 -p1

# Use system jar files instead of downloading from net
%patch2 -p1

%patch3 -p1

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath \
antlr \
jakarta-commons-collections \
commons-lang \
commons-logging \
tomcat6-servlet-2.5-api \
junit \
oro \
log4j \
jdom \
bcel \
werken.xpath \
hsqldb \
junit)
ant \
  -buildfile build/build.xml \
  -Dbuild.sysclasspath=first \
  jar javadocs test

# fix line-endings in generated files
sed -i 's/\r//' docs/api/stylesheet.css docs/api/package-list

# -----------------------------------------------------------------------------

%install
rm -rf %{buildroot}

# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}

# data
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr examples test %{buildroot}%{_datadir}/%{name}

# Maven metadata
install -pD -T -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap -a "%{name}:%{name}"

# -----------------------------------------------------------------------------


%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTICE README.txt
%{_javadir}/*.jar
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-%{name}.pom

%files manual
%doc LICENSE
%doc docs/*

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%files demo
%doc LICENSE
%{_datadir}/%{name}




%changelog
* Thu Feb 23 2012 Andrew Lukoshko <andrew.lukoshko@rosalab.ru> 0:1.6.4-1
- adopted for 2011.0
- spec updated with maven macroses
- RPM5 don't need clean section anymore

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.5-2.0.2mdv2009.0
+ Revision: 136570
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5-2.0.2mdv2008.1
+ Revision: 121046
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 09 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.5-2.0.1mdv2008.1
+ Revision: 116759
- fix BR werken.xpath is in main, werken-xpath is in contrib
- fix pom.xml (sync with jpp)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5-1.0.2mdv2008.0
+ Revision: 87243
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Sep 04 2007 David Walluck <walluck@mandriva.org> 0:1.5-1.0.1mdv2008.0
+ Revision: 78951
- 1.5


* Fri Mar 16 2007 Christiaan Welvaart <spturtle@mandriva.org> 0:1.4-4.3mdv2007.1
+ Revision: 144749
- rebuild for 2007.1
- Import velocity

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.4-4.1mdv2007.0
- bump release

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.4-3.2mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:1.4-3.1mdk
- release

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> 0:1.4-3jpp_1fc
- Build into Fedora.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.

* Tue Jun 07 2005 Gary Benson <gbenson@redhat.com>
- Build with servletapi5.
- Add NOTICE file as per Apache License version 2.0.
- Skip some failing tests.

* Tue Oct 19 2004 Fernando Nasser <fnasser@redhat.com> 0:1.4-3jpp_1rh
- First Red Hat build

* Fri Sep 24 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Adapt to jdom-1.0-1 replacing org.jdom.input.DefaultJDOMFactory
  by org.jdom.DefaultJDOMFactory in AnakiaJDOMFactory.java
  as well as using org.jdom.output.Format in AnakiaTask.java
- Therefore require jdom >= 0:1.0-1

* Fri Sep 03 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-2jpp
- Build with ant-1.6.2

* Tue Jun 08 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-1jpp
- 1.4 final
- Patch #0 is unnecessary (upstream)
- We have to build velocity against servletapi3
