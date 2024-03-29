# TODO
# - webapps
Summary:	DaveDAP's A Very Easy Directory Administration Program
Summary(pl.UTF-8):	DaveDAP - bardzo prosty program do administrowania katalogami
Name:		davedap
Version:	0.8.4
Release:	2
License:	GPL v2
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/davedap/%{name}-%{version}.tar.gz
# Source0-md5:	99abc5001ffe43dd8e9a26e19ac5c5f2
Source1:	%{name}.conf
URL:		http://davedap.sourceforge.net/
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	php(ldap)
Requires:	php(xml)
Requires:	webserver = apache
Requires:	webserver(php)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		davedapdir	%{_datadir}/%{name}

%description
DaveDAP is a web-based LDAP admin tool written in PHP. You can browse
your LDAP tree, create, delete, edit, and copy objects, perform
searches, and view your server's schema. You can even copy objects
between two LDAP servers and recursively delete or copy entire trees.

%description -l pl.UTF-8
DaveDAP to oparte na WWW narzędzie administracyjne do LDAP napisane w
PHP. Pozwala przeglądać drzewo LDAP, tworzyć, usuwać, modyfikować i
kopiować obiekty, wyszukiwać i oglądać schematy serwera. Można też
kopiować obiekty między dwoma serwerami LDAP i rekurencyjnie usuwać
lub kopiować całe drzewa.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{davedapdir}/{images,templates/creation}}

install *.php *.css *.txt *.js $RPM_BUILD_ROOT%{davedapdir}/
install images/*.png $RPM_BUILD_ROOT%{davedapdir}/images/
install templates/creation/*.php $RPM_BUILD_ROOT%{davedapdir}/templates/creation/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd
install config.php.example $RPM_BUILD_ROOT%{_sysconfdir}/davedap.conf
ln -s /etc/davedap.conf $RPM_BUILD_ROOT%{davedapdir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*davedap.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/davedap.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -v "^Include.*davedap.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
# there's no README, INSTALL may contain usefull info
%doc INSTALL
%dir %{davedapdir}
%{davedapdir}/images
%{davedapdir}/templates
%{davedapdir}/*.php
%{davedapdir}/*.js
%{davedapdir}/*.css
%{davedapdir}/*.txt
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
