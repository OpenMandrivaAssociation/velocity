# Copyright (c) 2000-2005, JPackage Project
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

Name:           velocity
Version:        1.6.4
Release:        4
Summary:        Java-based template engine
License:        ASL 2.0
URL:            http://velocity.apache.org/
Source0:        http://www.apache.org/dist/%{name}/engine/%{version}/%{name}-%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/org/apache/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Patch0:		velocity-remove-avalon-logkit.patch
Patch1:		velocity-use-system-jars.patch
Patch2:		velocity-servletapi5.patch
Patch3:		velocity-cleanup-pom.patch
Patch4:         velocity-tomcat6.patch
Group:          Development/Java
Requires:       apache-commons-collections
Requires:       apache-commons-logging
Requires:       apache-commons-lang
Requires:       tomcat6-servlet-2.5-api
Requires:       oro
Requires:	werken-xpath
Requires:       junit
Requires:       hsqldb
Requires:       jdom
Requires:       bcel
Requires:       log4j
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildRequires:	werken-xpath
BuildRequires:  ant
BuildRequires:  antlr
BuildRequires:  junit
BuildRequires:	ant-junit
BuildRequires:  hsqldb
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-lang
BuildRequires:  tomcat6-servlet-2.5-api
BuildRequires:  oro
BuildRequires:  jdom
BuildRequires:  bcel
BuildRequires:  log4j
BuildRequires:  jpackage-utils

# It fails one of the arithmetic test cases with gcj
BuildRequires:	java-devel >= 0:1.6.0
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
Requires:       jpackage-utils

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

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
%patch0 -p1

# Use system jars instead of downloading
%patch1 -p1

#Apply patch to remove explicit dependency on servletapi3
%patch2 -p1

# Remove (unavailable) parent reference and avalon-logkit from POM
cp %{SOURCE1} ./pom.xml
%patch3 -p1

# fix test for servlet api 2.5
%patch4 -p1

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath \
antlr \
apache-commons-collections \
commons-lang \
commons-logging \
tomcat6-servlet-2.5-api \
junit \
oro \
log4j \
jdom \
bcel \
werken-xpath \
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
cp -pr convert examples test %{buildroot}%{_datadir}/%{name}

# Maven metadata
install -pD -T -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.velocity %{name} %{version} JPP %{name}
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

# -----------------------------------------------------------------------------

%post
%update_maven_depmap

%postun
%update_maven_depmap

# -----------------------------------------------------------------------------

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.txt
%{_javadir}/*.jar
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*

%files manual
%defattr(-,root,root,-)
%doc LICENSE
%doc docs/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/%{name}

