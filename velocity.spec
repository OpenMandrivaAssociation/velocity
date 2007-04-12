%define section free
%define gcj_support 1

%define my_version 1.4
%define fileversion %{my_version}

Name:           velocity
Version:        %{my_version}
Release:        %mkrel 4.3
Epoch:          0
Summary:        Java-based template engine
License:        Apache License
Source:         velocity-1.4-RHCLEAN.tar.bz2
Patch0:		velocity-AnakiaJDOMFactory-jdom-DefaultJDOMFactory.patch
Patch1:		velocity-AnakiaTask-jdom-XMLOutputter.patch
Patch2:		velocity-servletapi5.patch
Patch3:		velocity-notexentests.patch
URL:            http://jakarta.apache.org/velocity/
Group:          Development/Java
Requires:       jakarta-commons-collections
Requires:       servletapi5
Requires:       oro
Requires:	werken.xpath
Requires:       jdom >= 0:1.0-1
Requires:       bcel
Requires:       log4j >= 0:1.1
Requires:       avalon-logkit
BuildRequires:	werken.xpath
BuildRequires:  ant
BuildRequires:  antlr
BuildRequires:  junit
BuildRequires:  jakarta-commons-collections
BuildRequires:  servletapi5
BuildRequires:  oro
BuildRequires:  jdom >= 0:1.0-1
BuildRequires:  bcel
BuildRequires:  log4j >= 0:1.1
BuildRequires:  avalon-logkit
BuildRequires:  jpackage-utils >= 0:1.5
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%prep
%setup -q -n %{name}-%{fileversion}
# Remove all binary libs used in compiling the package.
# Note that velocity has some jar files containing macros under
# examples and test that should not be removed.
find build -name '*.jar' -exec rm -f \{\} \;

%patch0 -b .sav
%patch1 -b .sav
%patch2 -p1
%patch3 -p1

%build
export CLASSPATH=$(build-classpath \
antlr \
jakarta-commons-collections \
servletapi5 \
avalon-logkit \
junit \
oro \
log4j \
jdom \
bcel \
werken.xpath)
%ant \
  -buildfile build/build.xml \
  -Djunit.jar=%{_javadir}/junit.jar \
  -Dbuild.sysclasspath=first \
  jar javadocs test

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 bin/%{name}-%{fileversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{fileversion}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{fileversion}*; do ln -sf ${jar} `echo $jar| sed "s|-%{fileversion}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{fileversion}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{fileversion}
rm -rf docs/api

# data
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr convert examples test $RPM_BUILD_ROOT%{_datadir}/%{name}

# fix
%{__perl} -pi -e 's/\r$//g' README.txt
find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*.sh" | \
  xargs %{__chmod} 755

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{fileversion} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTICE README.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc docs/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{fileversion}

%files demo
%defattr(-,root,root,0755)
%{_datadir}/%{name}

# -----------------------------------------------------------------------------


