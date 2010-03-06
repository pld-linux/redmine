# TODO
# - finish spec
# for reposman
%include	/usr/lib/rpm/macros.perl
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
rm -r vendor/plugins/ruby-net-ldap*
rm -r vendor/plugins/coderay*

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/lib/%{name},%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT{%{_bindir},%{perl_vendorlib}/Apache}

# This way any new files/features will not get accidentally lost on update
# as they will show in unpackaged files list
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/extra/mail_handler/rdm-mailhandler.rb $RPM_BUILD_ROOT%{_bindir}
#rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/extra/sample_plugin

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/extra/svn/reposman.rb $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/extra/svn/svnserve.wrapper $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/extra/svn/Redmine.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Apache

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/config $RPM_BUILD_ROOT%{_sysconfdir}
ln -s $RPM_BUILD_ROOT%{_sysconfdir}/config $RPM_BUILD_ROOT%{_datadir}/%{name}

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/{db,files,log,tmp} $RPM_BUILD_ROOT/var/lib/%{name}
ln -s /var/lib/%{name}/db $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/files $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/log $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/tmp $RPM_BUILD_ROOT%{_datadir}/%{name}

rm $RPM_BUILD_ROOT/var/lib/%{name}/*/delete.me

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
%doc README.rdoc doc public/dispatch.*.example config/*.example
%doc extra/sample_plugin
%dir %attr(755,redmine,root) %{_sysconfdir}/config
%attr(655,redmine,root) %{_sysconfdir}/config/*.rb
%attr(655,redmine,root) %{_sysconfdir}/config/*.yml
%dir %attr(755,redmine,root) %{_sysconfdir}/config/environments
%attr(655,redmine,root) %{_sysconfdir}/config/environments/demo.rb
%attr(655,redmine,root) %{_sysconfdir}/config/environments/development.rb
%attr(655,redmine,root) %{_sysconfdir}/config/environments/production.rb
%dir %attr(755,redmine,root) %{_sysconfdir}/config/initializers
%attr(755,redmine,root) %{_sysconfdir}/config/initializers/*.rb
%dir %attr(755,redmine,root) %{_sysconfdir}/config/locales
%attr(755,redmine,root) %{_sysconfdir}/config/locales/*.yml
%{_datadir}/%{name}/Rakefile
%{_datadir}/%{name}/app
%{_datadir}/%{name}/lib
%dir %{_datadir}/%{name}/public
%{_datadir}/%{name}/public/help
%{_datadir}/%{name}/public/images
%{_datadir}/%{name}/public/javascripts
%{_datadir}/%{name}/public/plugin_assets
%{_datadir}/%{name}/public/stylesheets
%{_datadir}/%{name}/public/themes
%{_datadir}/%{name}/public/*.html
%{_datadir}/%{name}/script
%{_datadir}/%{name}/vendor
%exclude %{_datadir}/%{name}/vendor/plugins/*/test
%dir %attr(755,redmine,root) /var/lib/%{name}
%dir %attr(755,redmine,root) /var/lib/%{name}/db
%dir %attr(755,redmine,root) /var/lib/%{name}/db/migrate
%attr(644,redmine,root) /var/lib/%{name}/db/migrate/*
%dir %attr(755,redmine,root) /var/lib/%{name}/files
%dir %attr(755,redmine,root) /var/lib/%{name}/log
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp/cache
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp/pids
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp/sessions
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp/sockets

%files testsuite
%defattr(644,root,root,755)
%{_datadir}/%{name}/config/environments/test*.rb
%{_datadir}/%{name}/test
%{_datadir}/%{name}/vendor/plugins/*/test
