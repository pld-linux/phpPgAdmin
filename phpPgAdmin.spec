# TODO
# - separate internal files (classes, libraries) and public files (.js, .css,
#   index.php) to htdocs and above and point docroot to htdocs dir
Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl.UTF-8):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	4.2.2
Release:	1
License:	GPL v2+
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	7716bd0b1afa8468e22b641bba8faa65
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Source3:	http://www.quarto.pl/~gotar/%{name}-jscalendar.tar.bz2
# Source3-md5:	84115f772a723cc742352c589df9af29
Patch0:		%{name}-config.patch
#Patch1:	%{name}-adodb.patch
Patch2:		%{name}-calendar.patch
URL:		http://phppgadmin.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
#Requires:	adodb >= 4.67-1.17
Requires:	php(pcre)
Requires:	php(pgsql)
Requires:	php(session)
Requires:	webapps
Requires:	webserver(php) >= 4.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procs).

%description -l pl.UTF-8
phpPgAdmin jest w pełni funkcjonalnym, bazowanym na WWW, narzędziem
administracyjnym dla serwera baz danych PostgreSQL. Posiada wszystkie
podstawowe możliwości, jak i część bardziej zaawansowanych jak
przełączniki, widoki i funkcje (procedury składowane).

%prep
%setup -q -a3
%patch0 -p1
#%patch1 -p1
%patch2 -p1
rm -f conf/config.inc.php-dist

# remove language source files (or one wants to make -devel subpackage?)
mv -f lang/translations.php .
rm -f lang/*.php
rm -f lang/{Makefile,synch,php2po,po2php,langcheck,convert.awk}
mv -f translations.php lang/translations.php
rm -f lang/recoded/README

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -a *.php *.txt *.js $RPM_BUILD_ROOT%{_appdir}
cp -a classes help images lang libraries themes xloadtree $RPM_BUILD_ROOT%{_appdir}
cp -a conf/*.php $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- %{name} < 4.0.1-1.2
# rescue app config
if [ -f /etc/phpPgAdmin/config.inc.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.inc.php{,.rpmnew}
	mv -f /etc/phpPgAdmin/config.inc.php.rpmsave %{_sysconfdir}/config.inc.php
fi

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*phpPgAdmin.conf/d" /etc/httpd/httpd.conf
	httpd_reload=1
fi

# change config version number for 4.1.2
if [ -f /etc/webapps/phpPgAdmin/config.inc.php ]; then
	echo "Adjusting configuration for phpPgAdmin 4.1.2"
	sed -i -e '/conf.*version/s/[0-9][0-9][\t ]*;/17;/' /etc/webapps/phpPgAdmin/config.inc.php
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/phpPgAdmin.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/phpPgAdmin.conf.rpmsave %{_sysconfdir}/httpd.conf
	httpd_reload=1
fi

# migrate from apache-config macros
if [ -f /etc/phpPgAdmin/apache-phpPgAdmin.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/phpPgAdmin/apache-phpPgAdmin.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/phpPgAdmin/apache-phpPgAdmin.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/phpPgAdmin/apache-phpPgAdmin.conf.rpmsave
fi

# place new config location, as trigger puts config only on first install, do it here.
# apache1
if [ -L /etc/apache/conf.d/99_phpPgAdmin.conf ]; then
	rm -f /etc/apache/conf.d/99_phpPgAdmin.conf
	/usr/sbin/webapp register apache %{_webapp}
	apache_reload=1
fi
# apache2
if [ -L /etc/httpd/httpd.conf/99_phpPgAdmin.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_phpPgAdmin.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	%service httpd reload
fi
if [ "$apache_reload" ]; then
	%service apache reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL TODO TRANSLATORS
%doc sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php

%{_appdir}
