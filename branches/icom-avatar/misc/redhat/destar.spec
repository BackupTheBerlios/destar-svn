Summary: Management Interface for the Asterisk PBX
Name: destar
Version: 0.3.0
Release: 1
License: GPL
Group: System Environment/Daemons
Source: %{name}-%{version}.tar.gz
URL: http://destar.berlios.de/
Buildroot: %{_tmppath}/%{name}-root
Requires: python python-quixote

%description
DeStar is a Web-based management and configuration tool for the Asterisk PBX.
DeStar's main features include hosted PBX and virtual PBX features which allow
you to have several PBXs on a single machine. Extensions can be managed for
SIP, IAX, Zap, and more.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_initrddir}
cp misc/redhat/init.d %{buildroot}%{_initrddir}/destar

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add destar

%preun
if [ $1 = 0 ]; then
        /sbin/service destar stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del destar
fi

%postun
if [ "$1" -ge "1" ]; then
        /sbin/service destar condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README.txt CHANGELOG.txt
/usr/sbin/*
/usr/share/*
%config(noreplace) /etc/*

%changelog
* Mon Feb 5 2007 Harald Holzer <harald@hholzer.at>
- initial spec.
