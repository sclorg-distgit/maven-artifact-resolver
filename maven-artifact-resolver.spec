%global pkg_name maven-artifact-resolver
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0
Release:        10.12%{?dist}
# Epoch is added because the original package's version in maven-shared is 1.1-SNAPSHOT
Epoch:          1
Summary:        Maven Artifact Resolution API
License:        ASL 2.0
URL:            http://maven.apache.org/shared/%{pkg_name}
Source0:        http://central.maven.org/maven2/org/apache/maven/shared/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}plexus-containers-component-metadata
BuildRequires:  %{?scl_prefix}maven-artifact-manager
BuildRequires:  %{?scl_prefix}maven-project
BuildRequires:  %{?scl_prefix}maven-shared


%description
Provides a component for plugins to easily resolve project dependencies.


%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# use plexus-component-metadata instead of old plugin
%pom_remove_plugin :plexus-maven-plugin
%pom_add_plugin org.codehaus.plexus:plexus-component-metadata pom.xml "
         <executions>
           <execution>
             <id>create-component-descriptor</id>
             <phase>generate-resources</phase>
             <goals>
              <goal>generate-metadata</goal>
             </goals>
           </execution>
         </executions>
"

%pom_add_dep org.apache.maven:maven-compat:1.0

# Incompatible method invocation
rm src/test/java/org/apache/maven/shared/artifact/resolver/DefaultProjectDependenciesResolverIT.java
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc DEPENDENCIES LICENSE NOTICE
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1:1.0-10.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1:1.0-10.11
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1:1.0-10.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1:1.0-10.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.4
- Remove requires on java

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-10.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.0-10
- Mass rebuild 2013-12-27

* Fri Aug 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.0-9
- Migrate away from mvn-rpmbuild (#997444)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Feb 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:1.0-7
- Add maven-shared to BR/R
- Add few other missing BRs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:1.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Sep 14 2012 Tomas Radej <tradej@redhat.com> - 1:1.0-4
- Installing folders separately with -m 755
- Installing NOTICE in javadoc subpackage
- Fixed changelog

* Wed Sep 12 2012 Tomas Radej <tradej@redhat.com> - 1:1.0-3
- Really fixed Provides/Obsoletes by introducing epoch

* Thu Sep 06 2012 Tomas Radej <tradej@redhat.com> - 1.0-2
- Fixed Provides/Obsoletes

* Tue Jul 31 2012 Tomas Radej <tradej@redhat.com> - 1.0-1
- Initial version
