# TODO
# - finish spec
Summary:	Flexible project management web application
Name:		redmine
Version:	0.9.3
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://rubyforge.org/frs/download.php/69449/%{name}-%{version}.tar.gz
# Source0-md5:	5a95eec4d26ec3819ffeff42137d5023
URL:		http://www.redmine.org/
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	ruby-rake >= 0.8.3
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	ruby-RMagic
Requires:	ruby-SyslogLogger
Requires:	ruby-coderay
Requires:	ruby-rails >= 2.3.5
Requires:	ruby-rubytree
Requires:	webapps
Requires:	webserver(alias)
Suggests:	cvs
Suggests:	git-core
Suggests:	mercurial
Suggests:	ruby-mocha
Suggests:	ruby-mysql
Suggests:	ruby-net-ldap
Suggests:	ruby-openid >= 2.1.4
Suggests:	subversion >= 1.3
Provides:	user(redmine)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Redmine is a flexible project management web application.

Overview:
- Multiple projects support
- Flexible role based access control.
- Flexible issue tracking system
- Gantt chart and calendar
- News, documents & files management
- Feeds & email notifications.
- Per project wiki
- Per project forums
- Simple time tracking functionality
- Custom fields for issues, projects and users
- SCM integration (SVN, CVS, Git, Mercurial, Bazaar and Darcs)
- Multiple LDAP authentication support
- User self-registration support
- Multilanguage support
- Multiple databases support

Written using Ruby on Rails framework, it is cross-platform and
cross-database.

%package testsuite
Summary:	Test suite for Redmine
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description testsuite
Test suite for Redmine.

%prep
%setup -q

rm -r vendor/gems
rm -f vendor/plugins/ruby-net-ldap*
rm -f vendor/plugins/coderay*

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 212 -d %{_datadir}/%{name} -s /bin/false -c "Redmine User" -g nobody redmine

%postun
if [ "$1" = "0" ]; then
	%userremove redmine
fi

%files
%defattr(644,root,root,755)
%{_datadir}/%{name}/app
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/public
%{_datadir}/%{name}/script
%{_datadir}/%{name}/vendor
%exclude %{_datadir}/%{name}/vendor/plugins/*/test

%files testsuite
%defattr(644,root,root,755)
%{_datadir}/%{name}/config/environments/test*.rb
%{_datadir}/%{name}/test
%{_datadir}/%{name}/vendor/plugins/*/test
