Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	3.1
Release:	1
License:	GPL v2+
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	b5c9added710f7831584196b8d3e4460
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/phppgadmin/
Requires:	php >= 4.0.6
Requires:	php-pcre
Requires:	php-pgsql >= 4.0.6
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pgadmindir	%{_datadir}/%{name}

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procs)

%description -l pl
phpPgAdmin jest w pelni funkcjonalnym bazowanym na WWW narzedziem
administracyjnym dla serwera baz danych PostgreSQL. Posiada wszystkie
podstawowe mozliwosc, jak i czesc bardziej zaawansowanych jak
przelaczniki, widoki i funkcje(zapisane procedury)

%prep
%setup -q -n phpPgAdmin

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pgadmindir}/{classes/{HTML_TreeMenu/images,database},images/themes/default,lang/recoded,libraries/adodb/{datadict,drivers},sql,themes/default},/etc/{%{name},httpd}}

install *.php *.js			$RPM_BUILD_ROOT%{_pgadmindir}
install classes/*.php			$RPM_BUILD_ROOT%{_pgadmindir}/classes
install classes/HTML_TreeMenu/TreeMenu.* $RPM_BUILD_ROOT%{_pgadmindir}/classes/HTML_TreeMenu
install classes/HTML_TreeMenu/images/*	$RPM_BUILD_ROOT%{_pgadmindir}/classes/HTML_TreeMenu/images
install classes/database/*.php		$RPM_BUILD_ROOT%{_pgadmindir}/classes/database
install images/themes/default/*.png	$RPM_BUILD_ROOT%{_pgadmindir}/images/themes/default
install lang/*.php			$RPM_BUILD_ROOT%{_pgadmindir}/lang
install lang/recoded/*.php		$RPM_BUILD_ROOT%{_pgadmindir}/lang/recoded
install libraries/*.php			$RPM_BUILD_ROOT%{_pgadmindir}/libraries
install libraries/adodb/*.php		$RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb
install libraries/adodb/datadict/*.php	$RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb/datadict
install libraries/adodb/drivers/*.php	$RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb/drivers
install sql/*.sql			$RPM_BUILD_ROOT%{_pgadmindir}/sql
install themes/default/*.css		$RPM_BUILD_ROOT%{_pgadmindir}/themes/default

install conf/*.php			$RPM_BUILD_ROOT/etc/%{name}
ln -s /etc/%{name}			$RPM_BUILD_ROOT%{_pgadmindir}/conf

install %SOURCE1 			$RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*phpPgAdmin.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/phpPgAdmin.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -v "^Include.*phpPgAdmin.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS DEVELOPERS FAQ HISTORY INSTALL TODO TRANSLATORS
%dir /etc/%{name}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) /etc/%{name}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%{_pgadmindir}
