Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	3.5.1
Release:	1
License:	GPL v2+
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	002ce3f34b06472eb1b35c8423b5b0e5
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/phppgadmin/
Requires:	php >= 4.1
Requires:	php-pcre
Requires:	php-pgsql >= 4.1
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pgadmindir	%{_datadir}/%{name}
%define		_config_http	/etc/httpd

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procs).

%description -l pl
phpPgAdmin jest w pe³ni funkcjonalnym, bazowanym na WWW, narzêdziem
administracyjnym dla serwera baz danych PostgreSQL. Posiada wszystkie
podstawowe mo¿liwo¶ci, jak i czê¶æ bardziej zaawansowanych jak
prze³±czniki, widoki i funkcje (procedury sk³adowane).

%prep
%setup -q -n phpPgAdmin

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pgadmindir}/{classes/{HTML_TreeMenu/images,database},help,images/themes/default,lang/recoded,libraries/adodb/{datadict,drivers},sql,themes/default},/etc/{%{name},httpd/httpd.conf}}

install *.php *.js *.txt		$RPM_BUILD_ROOT%{_pgadmindir}
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
# DONT MARK IT AS %DOC
install	help/*.php			$RPM_BUILD_ROOT%{_pgadmindir}/help
install conf/*.php			$RPM_BUILD_ROOT/etc/%{name}
ln -s /etc/%{name}			$RPM_BUILD_ROOT%{_pgadmindir}/conf

install %{SOURCE1} 			$RPM_BUILD_ROOT%{_config_http}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL TODO TRANSLATORS
%dir /etc/%{name}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) /etc/%{name}/*
%config(noreplace) %verify(not size mtime md5) %{_config_http}/%{name}.conf
%{_pgadmindir}
