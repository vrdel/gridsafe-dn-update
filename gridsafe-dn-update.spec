Name:           gridsafe-dn-update
Version:        0.1
Release:        1%{?dist}.srce
Summary:        Package provides simple script that synchronizes GridSAFE WebAcct's tomcat-users.xml cert DNs with ones found in Globus gridmap file.
License:        GPL
Vendor:         SRCE 
Source0:        gridsafe-dn-update-%{version}.tar.gz
BuildArch:      noarch
Requires:       python
Requires:       gridsafe-ige-server

%description
Package provides simple script that synchronizes GridSAFE WebAcct's
tomcat-users.xml cert's DNs with ones found in Globus gridmap file so it's
ensured that all users of CRO-NGI can authenticate to WebAcct with their X509
certificates.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0644,root,root) %{_sysconfdir}/cron.d/tomcat-dn-update

%changelog
* Wed Sep 9 2015 Daniel Vrcic <dvrcic@srce.hr> - 0.1-1%{?dist}
- initial version
