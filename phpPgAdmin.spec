Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	3.0
Release:	0.1
License:	GPL v2+
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	c0e04a526c2d9e88f865f3a740f02b60
URL:		http://sourceforge.net/projects/phppgadmin/
Requires:	php >= 4.0.6
Requires:	php-pcre
Requires:	php-pgsql >= 4.0.6
Requires:	webserver
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pgadmindir	/home/services/httpd/html/pgadmin

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
install -d $RPM_BUILD_ROOT%{_pgadmindir}/{classes,conf,images,lang,libraries,sql,themes}
install -d $RPM_BUILD_ROOT%{_pgadmindir}/classes/{HTML_TreeMenu/images,database}
install -d $RPM_BUILD_ROOT%{_pgadmindir}/images/themes/default
install -d $RPM_BUILD_ROOT%{_pgadmindir}/lang/recoded
install -d $RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb/{datadict,drivers}
install -d $RPM_BUILD_ROOT%{_pgadmindir}/themes/default

install *.php                            $RPM_BUILD_ROOT%{_pgadmindir}
install classes/*.php                    $RPM_BUILD_ROOT%{_pgadmindir}/classes
install classes/HTML_TreeMenu/TreeMenu.* $RPM_BUILD_ROOT%{_pgadmindir}/classes/HTML_TreeMenu
install classes/HTML_TreeMenu/images/*   $RPM_BUILD_ROOT%{_pgadmindir}/classes/HTML_TreeMenu/images
install classes/database/*.php           $RPM_BUILD_ROOT%{_pgadmindir}/classes/database
install conf/*.php                       $RPM_BUILD_ROOT%{_pgadmindir}/conf
install images/themes/default/*.gif      $RPM_BUILD_ROOT%{_pgadmindir}/images/themes/default
install lang/*.php                       $RPM_BUILD_ROOT%{_pgadmindir}/lang
install lang/recoded/*.php               $RPM_BUILD_ROOT%{_pgadmindir}/lang/recoded
install libraries/*.php                  $RPM_BUILD_ROOT%{_pgadmindir}/libraries
install libraries/adodb/*.php            $RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb
install libraries/adodb/datadict/*.php   $RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb/datadict
install libraries/adodb/drivers/*.php    $RPM_BUILD_ROOT%{_pgadmindir}/libraries/adodb/drivers
install sql/*.sql                        $RPM_BUILD_ROOT%{_pgadmindir}/sql
install themes/default/*.css             $RPM_BUILD_ROOT%{_pgadmindir}/themes/default

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS DEVELOPERS FAQ HISTORY INSTALL LICENSE TODO TRANSLATORS
%dir %{_pgadmindir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_pgadmindir}/conf/config.inc.php
%{_pgadmindir}/*
