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
BuildRequires:	rake >= 0.8.3
Requires:	rails >= 2.3.5
Requires:	webapps
Requires:	webserver(alias)
Suggests:	cvs
Suggests:	git-core
Suggests:	mercurial
Suggests:	ruby-mysql
Suggests:	ruby-openid
Suggests:	ruby-rmagic
Suggests:	subversion >= 1.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/%{name}
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

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
