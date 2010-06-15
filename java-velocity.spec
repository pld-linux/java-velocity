#
# Conditional build:
%include	/usr/lib/rpm/macros.java

%define		srcname		velocity
Summary:	Java templating engine
Summary(pl.UTF-8):	Silnik szablonowania dla Javy
Name:		java-velocity
Version:	1.6.3
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://ftp.tpnet.pl/vol/d1/apache/velocity/engine/1.6.3/velocity-%{version}.tar.gz
# Source0-md5:	5fee48e193cbc471c9a496c87ab06b9e
Patch0:		%{name}-nodownload.patch
URL:		http://velocity.apache.org
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	antlr
BuildRequires:	java(jdbc-stdext)
BuildRequires:	java(servlet)
BuildRequires:	java-avalon-logkit
BuildRequires:	java-commons-collections
BuildRequires:	java-commons-lang
BuildRequires:	java-commons-logging
BuildRequires:	java-log4j
BuildRequires:	java-oro
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	rpmbuild(macros) >= 1.555
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Java templating engine.

%description -l pl.UTF-8
Silnik szablonowania dla Javy.

%package doc
Summary:	Manual for %{srcname}
Summary(fr.UTF-8):	Documentation pour %{srcname}
Summary(it.UTF-8):	Documentazione di %{srcname}
Summary(pl.UTF-8):	Podręcznik dla %{srcname}
Group:		Documentation

%description doc
Documentation for %{srcname}.

%description doc -l fr.UTF-8
Documentation pour %{srcname}.

%description doc -l it.UTF-8
Documentazione di %{srcname}.

%description doc -l pl.UTF-8
Dokumentacja do %{srcname}.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package demo
Summary:	Demo for %{srcname}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{srcname}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{srcname}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{srcname}.

%package manual
Summary:	Tutorial for %{srcname}
Group:		Documentation

%description manual
Manual for %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}

%patch0 -p1

mkdir -p bin/lib

%build
export JAVA_HOME="%{java_home}"

required_jars="antlr avalon-logkit commons-collections commons-lang commons-logging jdom log4j oro servlet-api jdbc-stdext"
CLASSPATH=$(build-classpath $required_jars):../lib/werken-xpath-0.9.4.jar
cd build
%ant jar jar-src javadocs docs \
	-Dbuild.sysclasspath=first

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a bin/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a bin/%{srcname}-%{version}-sources.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%files doc
%defattr(644,root,root,755)
%doc bin/docs/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
