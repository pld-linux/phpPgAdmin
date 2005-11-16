Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	4.0	
Release:	1
License:	GPL v2+
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	9badba12100bd244e697c7448f57ab13
URL:		http://sourceforge.net/projects/phppgadmin/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires(triggerpostun):	sed >= 4.0
Requires:	php >= 4.1
Requires:	php-pcre
Requires:	php-pgsql >= 4.1
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	/usr/bin/awk /bin/bash /usr/bin/php
%define		_appdir		%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

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
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},%{_config_http}}

%{__sed} -i 's|error_reporting(E_ALL);|error_reporting(E_ALL \& ~E_NOTICE);|' libraries/lib.inc.php

cp -R * $RPM_BUILD_ROOT%{_appdir}
mv -f $RPM_BUILD_ROOT%{_appdir}/conf/* $RPM_BUILD_ROOT%{_sysconfdir}
rm -fr $RPM_BUILD_ROOT%{_appdir}/conf
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/conf

cat >> $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf <<EOF
# This is sample apache config
Alias /pgadmin /usr/share/phpPgAdmin
EOF

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%triggerpostun -- %{name} < 1.3.9-1.4
# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# nuke very-old config location (this mostly for Ra)
if [ ! -d /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# place new config location, as trigger puts config only on first install, do it here.
# apache1
if [ -d /etc/apache/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf /etc/apache/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi
# apache2
if [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL TODO TRANSLATORS
%dir %{_sysconfdir} 
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%{_appdir}
