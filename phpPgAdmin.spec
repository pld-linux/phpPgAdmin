Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	2.3.1
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Group(de):	Applikationen/Dateibanken/Schnittstellen
Group(pl):	Aplikacje/Bazy danych/Interfejsy
Source:		http://prdownloads.sourceforge.net/phppgadmin/%{name}_2-3-1.tar.gz
URL:		http://sourceforge.net/projects/phppgadmin/
Requires:	postgresql
Requires:	php >= 4
Requires:	webserver
Buildarch:	noarch
BuildRoot: 	/tmp/%{name}-%{version}-root


%define		_pgadmindir	/home/httpd/html/pgadmin

%description
phpPgAdmin is a fully functional web-based administration utility for a
PostgreSQL database server. It handles all the basic functionality as well
as some advanced features such as triggers, views and functions (stored
procs)

%description -l pl
phpPgAdmin jest w pelni funkcjonalnym bazowanym na WWW narzedziem
administracyjnym dla serwera baz danych PostgreSQL. Posiada wszystkie
podstawowe mozliwosc, jak i czesc bardziej zaawansowanych jak przelaczniki,
widoki i funkcje(zapisane procedury)

%prep
%setup -q -n phpPgAdmin
%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pgadmindir}/{lang,images,libraries}

cp *.php $RPM_BUILD_ROOT%{_pgadmindir}
cp *.html $RPM_BUILD_ROOT%{_pgadmindir}
cp images/*.gif $RPM_BUILD_ROOT%{_pgadmindir}/images

gzip -9nf Documentation.html BUGS DEVELOPERS INSTALL README TODO ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{_pgadmindir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_pgadmindir}/config.inc.php
%{_pgadmindir}/all_db.php
%{_pgadmindir}/db*.php
%{_pgadmindir}/fil*.php
%{_pgadmindir}/fun*.php
%{_pgadmindir}/grp*.php
%{_pgadmindir}/ldi*.php
%{_pgadmindir}/left.php
%{_pgadmindir}/main.php
%{_pgadmindir}/oper*.php
%{_pgadmindir}/rep*.php
%{_pgadmindir}/seq*.php
%{_pgadmindir}/sql.php
%{_pgadmindir}/tbl*.php
%{_pgadmindir}/trig*.php
%{_pgadmindir}/user*.php
%{_pgadmindir}/view*.php
%{_pgadmindir}/footer.inc.php
%{_pgadmindir}/header.inc.php
%{_pgadmindir}/index.php
%{_pgadmindir}/*.html
%{_pgadmindir}/images
%{_pgadmindir}/chinese*.php
%{_pgadmindir}/danish*.php
%{_pgadmindir}/catala*.php
%{_pgadmindir}/english*.php
%{_pgadmindir}/german*.php
%{_pgadmindir}/italian*.php
%{_pgadmindir}/lib.inc.php
%{_pgadmindir}/login*.php
%{_pgadmindir}/old.chinese*.php
%{_pgadmindir}/portu*.php
%{_pgadmindir}/russ*.php
%{_pgadmindir}/spanish*.php
