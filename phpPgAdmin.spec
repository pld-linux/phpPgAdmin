Summary:	phpPgAdmin - web-based PostgreSQL administration
Summary(pl):	phpPgAdmin - administracja bazami PostgreSQL przez WWW
Name:		phpPgAdmin
Version:	2.4.1
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://prdownloads.sourceforge.net/phppgadmin/%{name}_2-4.tar.bz2
URL:		http://sourceforge.net/projects/phppgadmin/
Requires:	php >= 4.0.6
Requires:	php-pgsql >= 4.0.6
Requires:	webserver
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pgadmindir	/home/httpd/html/pgadmin

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
%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pgadmindir}/{lang,images,libraries}

cp *.php *.html $RPM_BUILD_ROOT%{_pgadmindir}
cp config.inc.php-dist $RPM_BUILD_ROOT%{_pgadmindir}/config.inc.php
cp images/*.gif $RPM_BUILD_ROOT%{_pgadmindir}/images

gzip -9nf Documentation.html BUGS DEVELOPERS INSTALL README TODO ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{_pgadmindir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_pgadmindir}/config.inc.php
%{_pgadmindir}/[^c]*.php
%{_pgadmindir}/c[ah]*.php
%{_pgadmindir}/*.html
%{_pgadmindir}/images
