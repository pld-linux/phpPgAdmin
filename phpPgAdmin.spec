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
phpPgAdmin can administer a whole PostgreSQL-server (needs a
super-user) but also a single database. To accomplish the latter
you'll need a properly set up PostgreSQL-user who can read/write only
the desired database. It's up to you to look up the appropiate part in
the PostgreSQL manual. Currently phpPgAdmin can:
  - create and drop databases
  - create, copy, drop and alter tables
  - delete, edit and add fields
  - execute any SQL-statement, even batch-queries
  - manage keys on fields
  - load text files into tables
  - create (*) and read dumps of tables
  - export (*) and import data to CSV values
  - administer multiple servers and single databases
  - communicate in more than 20 different languages

%description -l pl
phpPgAdmin potrafi zarz±dzaæ ca³ymi bazami PostgreSQL (potrzebne
uprawnienia super-user'a) jak i pojedynczymi bazami danych. Bêdziesz
potrzebowa³ u¿ytkownika, który ma prawa zapisu/odczytu tylko tych baz,
którymi chcesz administrowaæ (zajrzyj do odpowiedniej czê¶ci manual'a
PostgreSQL). Aktualnie phpPgAdmin potrafi:
  - tworzyæ i usuwaæ bazy
  - create, copy, drop oraz alter na tabelach
  - dodawaæ, usuwaæ i edytowaæ pola
  - wykonywaæ dowolne zapytania SQL
  - zarz±dzaæ kluczami na rekordach
  - wczytywaæ tekst z plików do tabel
  - obs³ugiwaæ ponad 20 jêzyków
  - zarz±dzaæ wieloma serwerami i pojedyñczymi bazami danych
  - eksportowaæ i importowaæ dane do warto¶ci CSV
  - tworzyæ i czytaæ zrzuty tabel

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
