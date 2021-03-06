# TODO:
#	- other operation modes: rails/webrick, mongrel?\
#
# for reposman
Summary:	Flexible project management web application
Name:		redmine
Version:	1.3.2
Release:	5
License:	GPL v2
Group:		Applications/WWW
Source0:	http://rubyforge.org/frs/download.php/75910/%{name}-%{version}.tar.gz
# Source0-md5:	49b5dc8a4d06b4db855fdda2e30c2a69
Source2:	%{name}.conf
# Shove UTF-8 down rails throat, needed for rails < 3
Source3:	%{name}-fix_params.rb
Source4:	%{name}-fix_renderable.rb
Source5:	%{name}-fix_utf.rb
Patch0:		%{name}-pld.patch
Patch1:		%{name}-ldap.patch
Patch2:		%{name}-utf-regex.patch
Patch3:		%{name}-nogems.patch
Patch4:		%{name}-maildomain.patch
Patch5:		%{name}-gantt.patch
Patch6:		%{name}-git-parse.patch
Patch7:		%{name}-tmail.patch
URL:		http://www.redmine.org/
BuildRequires:	dos2unix
BuildRequires:	perl-base
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	apache(mod_rails)
Requires:	ruby-RMagick
Requires:	ruby-SyslogLogger
Requires:	ruby-coderay >= 1.0.0
Requires:	ruby-i18n >= 0.4.2
Requires:	ruby-rails2 = 2.3.16
Requires:	ruby-rake
Requires:	ruby-rubytree >= 0.5.2
Requires:	webapps
Requires:	webserver(alias)
Suggests:	cvs
Suggests:	git-core
Suggests:	mercurial
Suggests:	ruby-net-ldap
Suggests:	ruby-mocha
Suggests:	ruby-mysql-library
Suggests:	ruby-openid >= 2.1.4
Suggests:	subversion >= 1.3
Provides:	user(redmine)
Conflicts:	apache-base < 2.4.0-1
# Does not work AT ALL with rails 3 currently
Conflicts:	ruby-rails >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

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

%package mailhandler
Summary:	Forward emails from email server to redmine
Group:		Applications/WWW

%description mailhandler
Reads an email from standard input and forward it to a Redmine server
through a HTTP request.

%package reposman
Summary:	SCM repository manager for redmine
Group:		Applications/WWW
Requires:	ruby-activeresource

%description reposman
SCM repository manager for redmine.

%package testsuite
Summary:	Test suite for Redmine
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description testsuite
Test suite for Redmine.

%prep
%setup -q

%{__rm} -r vendor/gems
%{__rm} -r vendor/plugins/ruby-net-ldap*
%{__rm} -r vendor/rails

find \( -name '*.rb' -o -name '*.rake' \) -print0 | xargs -0 dos2unix -k -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# ruby 1.9.3 became very strict about escaping
%{__sed} -i  -e 's/\([^\]\+\):\\\([^\]\+\)/\1:\\\\\2/g' \
	     -e 's/^\([^:]\+:\s*\)\([^"]*\)%\([^"]*\)$/\1"\2%\3"/g' \
	     config/locales/*.yml

find -type f -print0 | \
	xargs -0 %{__sed} -i -e 's,/usr/bin/env ruby,%{__ruby},' \
			     -e 's,/usr/local/bin/ruby,%{__ruby},'

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT{%{_bindir},%{perl_vendorlib}/Apache} \
	$RPM_BUILD_ROOT/var/lib/%{name}/{files,log,plugin_assets,tmp}

# Check if everything is installed on update!

cp -a Rakefile app lib public script test vendor $RPM_BUILD_ROOT%{_datadir}/%{name}

install -p public/dispatch.cgi.example $RPM_BUILD_ROOT%{_datadir}/%{name}/public/dispatch.cgi
install -p public/dispatch.fcgi.example $RPM_BUILD_ROOT%{_datadir}/%{name}/public/dispatch.fcgi

install -p extra/mail_handler/rdm-mailhandler.rb $RPM_BUILD_ROOT%{_bindir}

install -p extra/svn/reposman.rb $RPM_BUILD_ROOT%{_bindir}
install -p extra/svn/svnserve.wrapper $RPM_BUILD_ROOT%{_bindir}
install -p extra/svn/Redmine.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Apache

cp -a config $RPM_BUILD_ROOT%{_sysconfdir}
install -p config/additional_environment.rb.example $RPM_BUILD_ROOT%{_sysconfdir}/config/additional_environment.rb
install -p config/configuration.yml.example $RPM_BUILD_ROOT%{_sysconfdir}/config/configuration.yml
install -p config/database.yml.example $RPM_BUILD_ROOT%{_sysconfdir}/config/database.yml
install -p config/settings.yml $RPM_BUILD_ROOT%{_sysconfdir}/config/settings.yml
ln -s %{_sysconfdir}/config $RPM_BUILD_ROOT%{_datadir}/%{name}

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/config/initializers/fix_params.rb
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/config/initializers/fix_renderable.rb
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/config/initializers/fix_utf.rb

cp -a db $RPM_BUILD_ROOT/var/lib/%{name}
ln -s /var/lib/%{name}/db $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/files $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/log $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/tmp $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /var/lib/%{name}/plugin_assets $RPM_BUILD_ROOT%{_datadir}/%{name}/public

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/config/*.example
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/public/*.example

%{__sed} -i -e 's,^RAILS_ROOT = .*,RAILS_ROOT = "%{_datadir}/%{name}",' $RPM_BUILD_ROOT%{_sysconfdir}/config/boot.rb

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 212 -d %{_datadir}/%{name} -s /bin/false -c "Redmine User" -g nobody redmine

%post
%banner -e %{name} <<-EOF
You may need to update redmine database, to do this run
(assuming 'production' is the name of redmine rails environment):
cd %{_datadir}/%{name}
rake db:migrate RAILS_ENV=production 
EOF

%postun
if [ "$1" = "0" ]; then
	%userremove redmine
fi

%triggerin -- apache-base
%webapp_register httpd %{_webapp}
%addusertogroup -q redmine http

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.rdoc doc/* public/*.example config/*.example
%doc extra/sample_plugin extra/svn/create_views.sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %attr(755,redmine,root) %{_sysconfdir}/config
%attr(644,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.rb
%attr(640,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.yml
%dir %attr(755,redmine,root) %{_sysconfdir}/config/environments
%attr(644,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/environments/development.rb
%attr(644,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/environments/production.rb
%dir %attr(755,redmine,root) %{_sysconfdir}/config/initializers
%attr(644,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/initializers/*.rb
%dir %attr(755,redmine,root) %{_sysconfdir}/config/locales
%attr(644,redmine,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/locales/*.yml
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/public
%{_datadir}/%{name}/Rakefile
%{_datadir}/%{name}/app
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/public/help
%{_datadir}/%{name}/public/images
%{_datadir}/%{name}/public/javascripts
%{_datadir}/%{name}/public/plugin_assets
%{_datadir}/%{name}/public/stylesheets
%{_datadir}/%{name}/public/themes
%{_datadir}/%{name}/public/*.html
%{_datadir}/%{name}/public/favicon.ico
%attr(755,redmine,root) %{_datadir}/%{name}/public/dispatch.*
%dir %{_datadir}/%{name}/script
%dir %{_datadir}/%{name}/script/performance
%dir %{_datadir}/%{name}/script/process
%attr(755,root,root) %{_datadir}/%{name}/script/[a-o]*
%attr(755,root,root) %{_datadir}/%{name}/script/plugin
%attr(755,root,root) %{_datadir}/%{name}/script/[q-z]*
%attr(755,root,root) %{_datadir}/%{name}/script/performance/*
%attr(755,root,root) %{_datadir}/%{name}/script/process/*
%{_datadir}/%{name}/vendor
%exclude %{_datadir}/%{name}/vendor/plugins/*/test
%dir %attr(755,redmine,root) /var/lib/%{name}
%dir %attr(755,redmine,root) /var/lib/%{name}/db
%dir %attr(755,redmine,root) /var/lib/%{name}/db/migrate
%attr(644,redmine,root) /var/lib/%{name}/db/migrate/*
%dir %attr(755,redmine,root) /var/lib/%{name}/files
%dir %attr(755,redmine,root) /var/lib/%{name}/log
%dir %attr(755,redmine,root) /var/lib/%{name}/plugin_assets
%dir %attr(755,redmine,root) /var/lib/%{name}/tmp
%{_datadir}/%{name}/config
%{_datadir}/%{name}/db
%{_datadir}/%{name}/files
%{_datadir}/%{name}/log
%{_datadir}/%{name}/tmp

%files reposman
%defattr(644,root,root,755)
%doc extra/svn/create_views.sql
%attr(755,root,root) %{_bindir}/reposman.rb
%attr(755,root,root) %{_bindir}/svnserve.wrapper
%{perl_vendorlib}/Apache/Redmine.pm

%files mailhandler
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdm-mailhandler.rb

%files testsuite
%defattr(644,root,root,755)
%attr(655,redmine,root) %{_sysconfdir}/config/environments/test*.rb
%{_datadir}/%{name}/test
%{_datadir}/%{name}/vendor/plugins/*/test
