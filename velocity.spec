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

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section free


Name:           velocity
Version:        1.5
Release:        %mkrel 2.0.2
Epoch:          0
Summary:        Java-based template engine
License:        Apache Software License
Source0:        http://www.apache.org/dist/velocity/engine/1.5/velocity-1.5.tar.gz
Source1:        %{name}-%{version}.pom
Patch0:         velocity-build_xml.patch
URL:            http://velocity.apache.org/
Group:          Development/Java
Requires:       excalibur-avalon-logkit
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-lang
Requires:       jdom >= 0:1.0-1
Requires:       log4j >= 0:1.1
Requires:       jakarta-oro
# Use servletapi5 instead of servletapi5
Requires:       servletapi5
Requires:       werken.xpath

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  antlr
BuildRequires:  junit
BuildRequires:  hsqldb

BuildRequires:  excalibur-avalon-logkit
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-lang
BuildRequires:  jdom >= 0:1.0-1
BuildRequires:  log4j >= 0:1.1
BuildRequires:  jakarta-oro
# Use servletapi5 instead of servletapi5
BuildRequires:  servletapi5
BuildRequires:  werken.xpath

BuildRequires:  java-rpmbuild >= 0:1.7.2

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:     java-gcj-compat-devel
%endif

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
# Remove all binary libs used in compiling the package.
# Note that velocity has some jar files containing macros under
# examples and test that should not be removed.
find build -name '*.jar' -exec rm -f \{\} \;

%patch0 -b .sav

rm src/test/org/apache/velocity/test/VelocityServletTestCase.java

%{__perl} -pi -e 's/\r$//g' LICENSE

%build
# Use servletapi5 instead of servletapi5 in CLASSPATH
mkdir -p bin/test-lib
pushd bin/test-lib
ln -sf $(build-classpath hsqldb)
ln -sf $(build-classpath junit)
popd
mkdir -p bin/lib
pushd bin/lib
ln -sf $(build-classpath ant)
ln -sf $(build-classpath antlr)
ln -sf $(build-classpath excalibur/avalon-logkit)
ln -sf $(build-classpath commons-collections)
ln -sf $(build-classpath commons-lang)
ln -sf $(build-classpath jdom)
ln -sf $(build-classpath log4j)
ln -sf $(build-classpath oro)
ln -sf $(build-classpath servletapi5)
ln -sf $(build-classpath werken.xpath)
popd
##antlr-2.7.5.jar
##avalon-logkit-2.1.jar
##commons-collections-3.1.jar
##commons-lang-2.1.jar
##jdom-1.0.jar
##log4j-1.2.12.jar
##oro-2.0.8.jar
##servletapi-2.3.jar
##werken.xpath-0.9.4.jar

%{ant} \
  -buildfile build/build.xml \
  jar javadocs #test

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 bin/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%add_to_maven_depmap org.apache.velocity velocity %{version} JPP %{name}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf docs/api

# data
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr convert examples test $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTICE README.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%config(noreplace) %{_mavendepmapfragdir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/classloader.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc docs/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
