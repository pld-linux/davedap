Summary:	DaveDAP's A Very Easy Directory Administration Program
Name:		davedap
Version:	0.8.1
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	f7756e7a8201725ed7dff72968078a8e
Source1:	%{name}.conf
URL:		http://davedap.sourceforge.net/
Requires:	apache
Requires:	php-ldap
Requires:	php-xml
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	davedapdir	%{_datadir}/%{name}

%description
DaveDAP is a web-based LDAP admin tool written in PHP. You can browse
your LDAP tree, create, delete, edit, and copy objects, perform
searches, and view your server's schema. You can even copy objects
between two LDAP servers and recursively delete or copy entire trees.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{davedapdir}/{images,include}}

install *.php *.css *.txt *.example $RPM_BUILD_ROOT%{davedapdir}/
install images/* $RPM_BUILD_ROOT%{davedapdir}/images/

install %SOURCE1 $RPM_BUILD_ROOT/etc/httpd/

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
%doc INSTALL TODO
%dir %{davedapdir}
%{davedapdir}/images
%{davedapdir}/*.php
%{davedapdir}/*.css
%{davedapdir}/*.txt
%{davedapdir}/*.example
%config(noreplace) %verify(not mtime size md5) /etc/httpd/%{name}.conf
