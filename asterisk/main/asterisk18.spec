%define astapi 18

#%%define docdir /usr/share/doc/asterisk
%define logdir /var/log
%bcond_with misdn

Summary: Asterisk, The Open Source PBX
Name: asterisk18

# IF YOU CHANGE THIS VERSION, RESET THE RELEASE TO 1.
Version: 18.20.2

# SET THIS TO '1' IF THE VERSION HAS INCREASED

#        v--- Change that to 1
Release: 1%{?dist}
#        ^--- Change that to 1

License: GPL
Group: Utilities/System
Source: asterisk-%{version}.tar.gz
Source1: say.conf
Source2: asterisk.logrotate
Source3: acts.patch
Patch5: acts.patch
Patch6: lazymembers-18.16.0.patch
BuildRoot: %{_tmppath}/asterisk-%{version}-root
URL: http://www.asterisk.org
Vendor: Sangoma tech, Inc.
Packager: Franck Danard <pramarajan@sangoma.com>
Provides: asterisk
Conflicts: asterisk10
Conflicts: asterisk11
Conflicts: asterisk12
Conflicts: asterisk13
Conflicts: asterisk14
Conflicts: asterisk15
Conflicts: asterisk16
Conflicts: asterisk17
Provides: asterisk%{astapi}
BuildRequires: subversion
Requires: lua
BuildRequires: lua-devel
Requires: iksemel
BuildRequires: iksemel-devel
Requires: portaudio
BuildRequires: portaudio-devel
Requires: neon
BuildRequires: neon-devel
Requires: libxml2
BuildRequires: libxml2-devel
Requires: spandsp
BuildRequires: spandsp-devel
Requires: libical
BuildRequires: libical-devel
Requires: libsrtp
BuildRequires: libsrtp-devel
Requires: freeradius
Requires: radiusclient-ng
BuildRequires: radiusclient-ng-devel
Requires: jack-audio-connection-kit
BuildRequires: jack-audio-connection-kit-devel
Requires: libresample
BuildRequires: libresample-devel
Requires: openldap
BuildRequires: openldap-devel
Requires: sqlite
BuildRequires: sqlite-devel
Requires: sqlite2
BuildRequires: sqlite2-devel
Requires: unixODBC
BuildRequires: unixODBC-devel
Requires: libtool-ltdl
BuildRequires: libtool-ltdl-devel
BuildRequires: binutils-devel
Requires: libedit
BuildRequires: libedit-devel

#BuildRequires: asterisk-osp-devel

BuildRequires: xmlstarlet wget

# Libunbound is required for proper SRV/NAPTR support - see
# http://blogs.asterisk.org/2016/04/20/pjsip-dns-support/
# "Asterisk 14 will ship with two resolvers: unbound and system. The
# unbound resolver provides a more complete DNS experience including
# DNSSEC support but requires an external library, libunbound"
BuildRequires: unbound-devel
Requires: unbound-libs

%{?_without_optimizations:Requires: %{name}-debuginfo = %{version}-%{release}}
Requires: %{name}-core = %{version}-%{release}
%{!?_without_dahdi:Requires: %{name}-dahdi = %{version}-%{release}}
Requires: %{name}-doc = %{version}
Requires: %{name}-voicemail = %{version}-%{release}
Requires: asterisk-sounds-core-en-ulaw
BuildRequires: ncurses-devel
BuildRequires: libxml2-devel
BuildRequires: libuuid-devel
%{!?_without_newt:BuildRequires: newt-devel}
BuildConflicts: rh-postgresql-devel

%description
Asterisk is an open source PBX and telephony development platform.  Asterisk
can both replace a conventional PBX and act as a platform for the
development of custom telephony applications for the delivery of dynamic
content over a telephone; similar to how one can deliver dynamic content
through a web browser using CGI and a web server.

Asterisk supports a variety of telephony hardware including BRI, PRI, POTS,
and IP telephony clients using the Inter-Asterisk eXchange (IAX) protocol (e.g.
gnophone or miniphone).  For more information and a current list of supported
hardware, see http://www.asterisk.org

%package core
Summary: Asterisk core package without any "extras".
Group: Utilities/System
Provides: asterisk-core
Provides: asterisk%{astapi}-core
#Obsoletes: asterisk-core
Conflicts: asterisk10-core
Conflicts: asterisk11-core
Conflicts: asterisk12-core
Requires: openssl
Requires: libxml2
Requires(pre): %{_sbindir}/groupadd
Requires(pre): %{_sbindir}/useradd

%description core
This package contains a base install of Asterisk without any "extras".

#
#  Alsa subpackage
#
%{?_without_alsa:%if 0}
%{!?_without_alsa:%if 1}
%package alsa
Summary: Alsa channel driver for Asterisk
Group: Utilities/System
Provides: asterisk-alsa
Provides: asterisk%{astapi}-alsa
#Obsoletes: asterisk-alsa
%if "%{distname}" == "suse" || "%{distname}" == "sles"
BuildRequires: alsa-devel
Requires: alsa
%else
BuildRequires: alsa-lib-devel
Requires: alsa-lib
%endif
Requires: %{name}-core = %{version}-%{release}

%description alsa
Alsa channel driver for Asterisk
%endif

#
#  snmp subpackage
#
%{?_without_snmp:%if 0}
%{!?_without_snmp:%if 1}
%package snmp
Summary: snmp resource module for Asterisk
Group: Utilities/System
Provides: asterisk-snmp
Provides: asterisk%{astapi}-snmp
#Obsoletes: asterisk-snmp
%if "%{distname}" == "suse" || "%{distname}" == "sles"
BuildRequires: sensors
BuildRequires: tcpd-devel
%else
BuildRequires: lm_sensors-devel
%endif
BuildRequires: net-snmp-devel
Requires: net-snmp
Requires: %{name}-core = %{version}-%{release}

%description snmp
snmp resource module for Asterisk
%endif

#
#  pgsql subpackage
#
%{?_without_pgsql:%if 0}
%{!?_without_pgsql:%if 1}
%package pgsql
Summary: Postgresql modules for Asterisk
Group: Utilities/System
Provides: asterisk-pgsql
Provides: asterisk%{astapi}-pgsql
#Obsoletes: asterisk-pgsql
BuildRequires: postgresql-devel
Requires: postgresql
Requires: %{name}-core = %{version}-%{release}

%description pgsql
Postgresql modules for Asterisk
%endif

#
#  tds subpackage
#
%{?_without_tds:%if 0}
%{!?_without_tds:%if 1}
%package tds
Summary: tds modules for Asterisk
Group: Utilities/System
Provides: asterisk-tds
Provides: asterisk%{astapi}-tds
#Obsoletes: asterisk-tds
BuildRequires: freetds-devel
Requires: freetds
Requires: %{name}-core = %{version}-%{release}

%description tds
tds modules for Asterisk
%endif

#
#  dahdi subpackage
#
%{?_without_dahdi:%if 0}
%{!?_without_dahdi:%if 1}
%package dahdi
Summary: DAHDI channel driver for Asterisk
Group: Utilities/System
Provides: asterisk-dahdi
Provides: asterisk%{astapi}-dahdi
#Obsoletes: asterisk-dahdi
Requires: %{name}-core = %{version}-%{release}
BuildRequires: libopenr2-devel
BuildRequires: libpri-devel
BuildRequires: libss7-devel
BuildRequires: libtonezone-devel
BuildRequires: dahdi-linux-devel
# rem via bryan for pbxtended
#Requires: libopenr2
#Requires: libpri
#Requires: libss7
#Requires: libtonezone
#Requires: dahdi-linux
#Requires: dahdi-linux-kmod
AutoReqProv: no

%description dahdi
DAHDI channel driver for Asterisk
%endif

#
#  mISDN subpackage
#
%if %{with misdn}
%package misdn
Summary: mISDN channel driver for Asterisk
Group: Utilities/System
Provides: asterisk-misdn
Provides: asterisk%{astapi}-misdn
#Obsoletes: asterisk-misdn
Requires: %{name}-core = %{version}-%{release}
BuildRequires: mISDNuser-devel
BuildRequires: mISDN-devel
Requires: mISDNuser
Requires: mISDN
Requires: mISDN-kmod
AutoReqProv: no

%description misdn
mISDN channel driver for Asterisk
%endif

#
#  Configs subpackage
#
%package configs
Summary: Basic configuration files for Asterisk
Group: Utilities/System
Provides: asterisk-configs
Provides: asterisk%{astapi}-configs
#Obsoletes: asterisk-configs
Requires: %{name}-core = %{version}

%description configs
The sample configuration files for Asterisk

#
#  cURL subpackage
#
%{?_without_curl:%if 0}
%{!?_without_curl:%if 1}
%package curl
Summary: cURL application module for Asterisk
Group: Utilities/System
Provides: asterisk-curl
Provides: asterisk%{astapi}-curl
#Obsoletes: asterisk-curl
BuildRequires: curl-devel
Requires: curl
Requires: %{name}-core = %{version}-%{release}

%description curl
cURL application module for Asterisk
%endif

#
#  Development subpackage
#
%package devel
Summary: Static libraries and header files for Asterisk development
Group: Development/Libraries
Provides: asterisk-devel
Provides: asterisk%{astapi}-devel
#Obsoletes: asterisk-devel
Requires: %{name}-core = %{version}

%description devel
The static libraries and header files needed for building additional Asterisk
plugins/modules

#
#  Documentation subpackage
#
%package doc
Summary: Documentation files for Asterisk
Group: Development/Libraries
Provides: asterisk-doc
Provides: asterisk%{astapi}-doc
#Obsoletes: asterisk-doc
Requires: %{name}-core = %{version}

%description doc
The Documentation files for Asterisk

#
#  Ogg-Vorbis subpackage
#
%{?_without_ogg:%if 0}
%{!?_without_ogg:%if 1}
%package ogg
Summary: Ogg-Vorbis codec module for Asterisk
Group: Utilities/System
Provides: asterisk-ogg
Provides: asterisk%{astapi}-ogg
#Obsoletes: asterisk-ogg
BuildRequires: libvorbis-devel libogg-devel
Requires: libvorbis libogg
Requires: %{name}-core = %{version}-%{release}

%description ogg
Asterisk format plugin for the Ogg-Vorbis codec
%endif

#
#  Speex subpackage
#
%{?_without_speex:%if 0}
%{!?_without_speex:%if 1}
%package speex
Summary: Speex codec module for Asterisk
Group: Utilities/System
Provides: asterisk-speex
Provides: asterisk%{astapi}-speex
#Obsoletes: asterisk-speex
BuildRequires: speex-devel
Requires: speex
Requires: %{name}-core = %{version}-%{release}

%description speex
Asterisk format plugin for the Speex codec
%endif

#
#  resample subpackage
#
%package resample
Summary: resampling codec module for Asterisk
Group: Utilities/System
Provides: asterisk-resample
Provides: asterisk%{astapi}-resample
#Obsoletes: asterisk-resample
BuildRequires: libresample-devel
Requires: libresample
Requires: %{name}-core = %{version}-%{release}

%description resample
Asterisk plugin for the resample codec

#
#  unixODBC subpackage
#
%{?_without_odbc:%if 0}
%{!?_without_odbc:%if 1}
%package odbc
Summary: Open Database Connectivity (ODBC) drivers for Asterisk
Group: Utilities/System
Provides: asterisk-odbc
Provides: asterisk%{astapi}-odbc
#Obsoletes: asterisk-odbc
BuildRequires: unixODBC-devel
Requires: unixODBC
Requires: %{name}-core = %{version}-%{release}

%description odbc
ODBC drivers for Asterisk
%endif

#
#  sqlite3 subpackage
#
%{?_without_sqlite3:%if 0}
%{!?_without_sqlite3:%if 1}
%package sqlite3
Summary: sqlite3 drivers for Asterisk
Group: Utilities/System
Provides: asterisk-sqlite3
Provides: asterisk%{astapi}-sqlite3
#Obsoletes: asterisk-sqlite3
BuildRequires: sqlite-devel
Requires: sqlite
Requires: %{name}-core = %{version}-%{release}

%description sqlite3
sqlite3 drivers for Asterisk
%endif

#
#  voicemail file storage subpackage
#
%package voicemail
Summary: Voicemail with file storage module for Asterisk
Group: Utilities/System
Provides: asterisk-voicemail = %{version}-%{release}
Provides: asterisk%{astapi}-voicemail
Provides: asterisk-voicemail-filestorage = %{version}-%{release}
Provides: asterisk%{astapi}-voicemail-filestorage
#Obsoletes: asterisk-voicemail
#Obsoletes: asterisk-voicemail-filestorage
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-voicemail-filestorage = %{version}-%{release}
Conflicts: %{name}-voicemail-odbcstorage
Conflicts: %{name}-voicemail-imapstorage

%description voicemail
Voicemail with file storage module for Asterisk

#
#  voicemail ODBC storage subpackage
#
%{?_without_voicemail_odbcstorage:%if 0}
%{!?_without_voicemail_odbcstorage:%if 1}
%package voicemail-odbcstorage
Summary: Voicemail with ODBC storage module for Asterisk
Group: Utilities/System
Provides: asterisk-voicemail-odbcstorage = %{version}-%{release}
Provides: asterisk%{astapi}-voicemail-odbcstorage
#Obsoletes: asterisk-voicemail-odbcstorage
BuildRequires: unixODBC-devel
Requires: unixODBC
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-voicemail = %{version}-%{release}
Conflicts: %{name}-voicemail-filestorage
Conflicts: %{name}-voicemail-imapstorage

%description voicemail-odbcstorage
Voicemail with ODBC storage module for Asterisk
%endif

#
#  voicemail IMAP storage subpackage
#
%{?_without_voicemail_imapstorage:%if 0}
%{!?_without_voicemail_imapstorage:%if 1}
%package voicemail-imapstorage
Summary: Voicemail with IMAP storage module for Asterisk
Group: Utilities/System
Provides: asterisk-voicemail-imapstorage = %{version}-%{release}
Provides: asterisk%{astapi}-voicemail-imapstorage
#Obsoletes: asterisk-voicemail-imapstorage
%if "%{distname}" == "suse" || "%{distname}" == "sles"
BuildRequires: imap-devel
Requires: imap-lib
%else
BuildRequires: libc-client-devel
Requires: libc-client
%endif
Requires: %{name}-core = %{version}-%{release}
Provides: %{name}-voicemail = %{version}-%{release}
Conflicts: %{name}-voicemail-filestorage
Conflicts: %{name}-voicemail-odbcstorage

%description voicemail-imapstorage
Voicemail with IMAP storage module for Asterisk
%endif

#
#  addons subpackage
#
%package addons
Summary: Asterisk-addons package.
Group: Utilities/System
Requires: asterisk%{astapi}-addons-core = %{version}-%{release}
Provides: asterisk-addons
Provides: asterisk%{astapi}-addons

Requires: %{name}-addons-core = %{version}-%{release}

%{?_without_mysql:%if 0}
%{!?_without_mysql:%if 1}
Requires: %{name}-addons-mysql = %{version}-%{release}
Requires: mysql
%endif

%{?_without_bluetooth:%if 0}
%{!?_without_bluetooth:%if 1}
Requires: %{name}-addons-bluetooth = %{version}-%{release}
Requires: bluez-libs
%endif

%{?_without_ooh323:%if 0}
%{!?_without_ooh323:%if 1}
Requires: %{name}-addons-ooh323 = %{version}-%{release}
%endif

%description addons
This package contains a base install of Asterisk-addons without any "extras".

#
#  addons-core subpackage
#
%package addons-core
Summary: Asterisk-addons core package.
Group: Utilities/System
Provides: asterisk-gplonly
Requires: asterisk%{astapi}-core = %{version}-%{release}
Provides: asterisk-addons-core
Provides: asterisk%{astapi}-addons-core

%description addons-core
This package contains a base install of Asterisk-addons without any "extras".

#
#  addons-mysql subpackage
#
%{?_without_mysql:%if 0}
%{!?_without_mysql:%if 1}
%package addons-mysql
Summary: mysql modules for Asterisk
Group: Utilities/System
BuildRequires: mysql-devel
Requires: mysql
Requires: %{name}-addons-core = %{version}-%{release}
Provides: asterisk-addons-mysql
Provides: asterisk%{astapi}-addons-mysql

%description addons-mysql
mysql modules for Asterisk
%endif

#
#  bluetooth subpackage
#
%{?_without_bluetooth:%if 0}
%{!?_without_bluetooth:%if 1}
%package addons-bluetooth
Summary: bluetooth modules for Asterisk
Group: Utilities/System
BuildRequires: bluez-libs-devel
Requires: bluez-libs
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk-addons-bluetooth
Provides: asterisk%{astapi}-addons-bluetooth

%description addons-bluetooth
bluetooth modules for Asterisk
%endif

#
#  ooh323 subpackage
#
%{?_without_ooh323:%if 0}
%{!?_without_ooh323:%if 1}
%package addons-ooh323
Summary: chan_ooh323 module for Asterisk
Group: Utilities/System
Requires: %{name}-core = %{version}-%{release}
Provides: asterisk-addons-ooh323
Provides: asterisk%{astapi}-addons-ooh323

%description addons-ooh323
chan_ooh323 module for Asterisk
%endif

%prep
%setup -n asterisk-%{version}

%patch5 -p0
%patch6 -p1

%build
%ifarch x86_64
%define makeflags OPT=-fPIC
%else
%define makeflags OPT=
%endif
echo %{version}%{?_without_optimizations:-debug} > .version

#pjproject is automatically enabled in asterisk 16 and above and no longer needs
#to be bundled here. These builds should be treated as if --with-pjproject-bundled
#is set
./configure --libdir=%{_libdir} --with-jansson-bundled
make menuselect.makeopts
#menuselect/menuselect --list-options to get the options passed below
%if !%{with misdn}
menuselect/menuselect --disable-category MENUSELECT_CORE_SOUNDS --disable-category MENUSELECT_EXTRA_SOUNDS --disable-category MENUSELECT_MOH --enable-category MENUSELECT_ADDONS --enable res_pktccops --enable chan_mgcp --enable chan_motif --enable app_meetme --enable app_page --enable res_snmp --enable res_srtp --disable BUILD_NATIVE --enable DONT_OPTIMIZE --enable res_chan_stats --enable res_endpoint_stats --enable codec_opus --enable codec_silk --enable codec_siren7 --enable codec_siren14 --enable app_macro --enable app_voicemail_odbc --enable app_voicemail_imap --disable chan_misdn menuselect.makeopts
%else
menuselect/menuselect --disable-category MENUSELECT_CORE_SOUNDS --disable-category MENUSELECT_EXTRA_SOUNDS --disable-category MENUSELECT_MOH --enable-category MENUSELECT_ADDONS --enable res_pktccops --enable chan_mgcp --enable chan_motif --enable app_meetme --enable app_page --enable res_snmp --enable res_srtp --disable BUILD_NATIVE --enable DONT_OPTIMIZE --enable res_chan_stats --enable res_endpoint_stats --enable codec_opus --enable codec_silk --enable codec_siren7 --enable codec_siren14 --enable app_macro --enable app_voicemail_odbc --enable app_voicemail_imap --enable chan_misdn menuselect.makeopts
%endif

contrib/scripts/get_mp3_source.sh

make %{?_smp_mflags} %{makeflags}

%install
echo DEBUG
pwd

mkdir -p $RPM_BUILD_ROOT/home/asterisk/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/
echo "AST_USER=asterisk" > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/asterisk
echo "AST_GROUP=asterisk" >> $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/asterisk
echo "COREDUMP=yes" >> $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/asterisk

make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT samples
make DESTDIR=$RPM_BUILD_ROOT config

# For some reason, when the opus xml doc file is in thirdparty,
# asterisk can't find it and crashes.
mv -f $RPM_BUILD_ROOT/var/lib/asterisk/documentation/thirdparty/*xml $RPM_BUILD_ROOT/var/lib/asterisk/documentation/

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/asterisk
echo -e "#This comment is to fix rpm file replacing\n#Config file built on $(date)" >> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/asterisk

mkdir -p $RPM_BUILD_ROOT/var/lib/asterisk/licenses/
mkdir -p $RPM_BUILD_ROOT/var/lib/digium/licenses/

mkdir -p %{buildroot}%{_includedir}/asterisk/
cp include/asterisk.h %{buildroot}%{_includedir}/
cp -r include/asterisk/*.h %{buildroot}%{_includedir}/asterisk/

cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk

%pre core
# Make sure the 'asterisk' user exists
getent group asterisk >/dev/null || groupadd -g 995 -r asterisk
getent passwd asterisk >/dev/null || useradd -r -u 995 -g asterisk -s /bin/bash -d /home/asterisk asterisk

%post core
# sng7 - asterisk is started by fwconsole
chkconfig --del asterisk || :
systemctl disable asterisk || :

#shmz ha install, so treat it as such and redo the links
if [ -e /etc/schmooze/pbx-ha -a -f /etc/drbd.d/asterisk.res ]; then
	[ ! -h /var/log/asterisk ] && ( rm -rf /var/log/asterisk; ln -s /drbd/asterisk/log /var/log/asterisk )
	[ ! -h /var/spool/asterisk ] && ( rm -rf /var/spool/asterisk ; ln -s /drbd/asterisk/spool /var/spool/asterisk )
	[ ! -h /var/lib/asterisk ] && ( rm -rf /var/lib/asterisk; ln -s /drbd/asterisk/lib /var/lib/asterisk )
	[ ! -h /etc/asterisk ] && ( rm -rf /etc/asterisk; ln -s /drbd/asterisk/etcasterisk /etc/asterisk )
else
	touch /etc/asterisk/ari.conf
	touch /etc/asterisk/ari_general_additional.conf
	touch /etc/asterisk/ari_general_custom.conf
	touch /etc/asterisk/ari_additional.conf
	touch /etc/asterisk/ari_additional_custom.conf
	# Ignore errors
	chown asterisk.asterisk /etc/asterisk/ari* || :
	#https://issues.freepbx.org/browse/FREEPBX-18261
	touch /etc/asterisk/smdi.conf
	touch /etc/asterisk/statsd.conf
	# Ignore errors
	chown asterisk.asterisk /etc/asterisk/smdi* || :
	chown asterisk.asterisk /etc/asterisk/statsd* || :
fi

%post
rm -f /etc/logrotate.d/asterisk.rpm*.*

%clean
cd $RPM_BUILD_DIR
%{__rm} -rf asterisk-%{version}
%{__rm} -rf /var/log/%{name}-sources-%{version}-%{release}.make.err
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%files core
%defattr(-, root, root)
%config %{_sysconfdir}/rc.d/init.d/asterisk
%config %{_sysconfdir}/sysconfig/asterisk
%attr(0775,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(0755,asterisk,asterisk) %dir /home/asterisk
%{_libdir}/asterisk/modules/app_adsiprog.so
%{_libdir}/asterisk/modules/app_alarmreceiver.so
%{_libdir}/asterisk/modules/app_amd.so
%{_libdir}/asterisk/modules/app_attended_transfer.so
%{_libdir}/asterisk/modules/app_audiosocket.so
%{_libdir}/asterisk/modules/app_authenticate.so
%{_libdir}/asterisk/modules/app_blind_transfer.so
%{_libdir}/asterisk/modules/app_broadcast.so
%{_libdir}/asterisk/modules/app_bridgeaddchan.so
%{_libdir}/asterisk/modules/app_cdr.so
%{_libdir}/asterisk/modules/app_celgenuserevent.so
%{_libdir}/asterisk/modules/app_chanisavail.so
%{_libdir}/asterisk/modules/app_channelredirect.so
%{_libdir}/asterisk/modules/app_chanspy.so
%{_libdir}/asterisk/modules/app_confbridge.so
%{_libdir}/asterisk/modules/app_controlplayback.so
%{_libdir}/asterisk/modules/app_db.so
%{_libdir}/asterisk/modules/app_dial.so
%{_libdir}/asterisk/modules/app_dictate.so
%{_libdir}/asterisk/modules/app_directed_pickup.so
%{_libdir}/asterisk/modules/app_directory.so
%{_libdir}/asterisk/modules/app_disa.so
%{_libdir}/asterisk/modules/app_dumpchan.so
%{_libdir}/asterisk/modules/app_echo.so
%{_libdir}/asterisk/modules/app_exec.so
%{_libdir}/asterisk/modules/app_externalivr.so
%{_libdir}/asterisk/modules/app_festival.so
%{_libdir}/asterisk/modules/app_forkcdr.so
%{_libdir}/asterisk/modules/app_followme.so
%{_libdir}/asterisk/modules/app_getcpeid.so
%{_libdir}/asterisk/modules/app_ices.so
%{_libdir}/asterisk/modules/app_if.so
%{_libdir}/asterisk/modules/app_image.so
%{_libdir}/asterisk/modules/app_macro.so
%{_libdir}/asterisk/modules/app_milliwatt.so
%{_libdir}/asterisk/modules/app_minivm.so
%{_libdir}/asterisk/modules/app_mixmonitor.so
%{_libdir}/asterisk/modules/app_morsecode.so
%{_libdir}/asterisk/modules/app_mp3.so
%{_libdir}/asterisk/modules/app_nbscat.so
%{_libdir}/asterisk/modules/app_originate.so
%{_libdir}/asterisk/modules/app_playback.so
%{_libdir}/asterisk/modules/app_playtones.so
%{_libdir}/asterisk/modules/app_privacy.so
%{_libdir}/asterisk/modules/app_queue.so
%{_libdir}/asterisk/modules/app_readexten.so
%{_libdir}/asterisk/modules/app_read.so
%{_libdir}/asterisk/modules/app_record.so
%{_libdir}/asterisk/modules/app_sayunixtime.so
%{_libdir}/asterisk/modules/app_senddtmf.so
%{_libdir}/asterisk/modules/app_sendtext.so
%{_libdir}/asterisk/modules/app_signal.so
%{_libdir}/asterisk/modules/app_sms.so
%{_libdir}/asterisk/modules/app_softhangup.so
%{_libdir}/asterisk/modules/app_speech_utils.so
%{_libdir}/asterisk/modules/app_stack.so
%{_libdir}/asterisk/modules/app_system.so
%{_libdir}/asterisk/modules/app_talkdetect.so
%{_libdir}/asterisk/modules/app_test.so
%{_libdir}/asterisk/modules/app_transfer.so
%{_libdir}/asterisk/modules/app_url.so
%{_libdir}/asterisk/modules/app_userevent.so
%{_libdir}/asterisk/modules/app_verbose.so
%{_libdir}/asterisk/modules/app_waitforring.so
%{_libdir}/asterisk/modules/app_waitforsilence.so
%{_libdir}/asterisk/modules/app_waituntil.so
%{_libdir}/asterisk/modules/app_while.so
%{_libdir}/asterisk/modules/app_zapateller.so

%{_libdir}/asterisk/modules/app_dtmfstore.so
%{_libdir}/asterisk/modules/app_reload.so
%{_libdir}/asterisk/modules/app_waitforcond.so

%{_libdir}/asterisk/modules/bridge_builtin_features.so
%{_libdir}/asterisk/modules/bridge_simple.so
%{_libdir}/asterisk/modules/bridge_softmix.so
%{_libdir}/asterisk/modules/cdr_csv.so
%{_libdir}/asterisk/modules/cdr_custom.so
%{_libdir}/asterisk/modules/cdr_manager.so
%{_libdir}/asterisk/modules/cel_custom.so
%{_libdir}/asterisk/modules/cel_manager.so
%{_libdir}/asterisk/modules/chan_audiosocket.so
%{_libdir}/asterisk/modules/chan_iax2.so
%{_libdir}/asterisk/modules/chan_mgcp.so
%{_libdir}/asterisk/modules/chan_rtp.so
%{_libdir}/asterisk/modules/chan_oss.so
%{_libdir}/asterisk/modules/chan_phone.so
%{_libdir}/asterisk/modules/chan_skinny.so
%{_libdir}/asterisk/modules/chan_sip.so
%{_libdir}/asterisk/modules/chan_unistim.so
%{_libdir}/asterisk/modules/codec_adpcm.so
%{_libdir}/asterisk/modules/codec_alaw.so
%{_libdir}/asterisk/modules/codec_a_mu.so
%{_libdir}/asterisk/modules/codec_g722.so
%{_libdir}/asterisk/modules/codec_g726.so
%{_libdir}/asterisk/modules/codec_gsm.so
%{_libdir}/asterisk/modules/codec_ilbc.so
%{_libdir}/asterisk/modules/codec_lpc10.so
%{_libdir}/asterisk/modules/codec_ulaw.so

%{_libdir}/asterisk/modules/codec_opus.so
%{_libdir}/asterisk/modules/codec_silk.so
%{_libdir}/asterisk/modules/codec_siren7.so
%{_libdir}/asterisk/modules/codec_siren14.so
%{_libdir}/asterisk/modules/codec_*manifest.xml

%{_libdir}/asterisk/modules/format_g719.so
%{_libdir}/asterisk/modules/format_g723.so
%{_libdir}/asterisk/modules/format_g726.so
%{_libdir}/asterisk/modules/format_g729.so
%{_libdir}/asterisk/modules/format_gsm.so
%{_libdir}/asterisk/modules/format_h263.so
%{_libdir}/asterisk/modules/format_h264.so
%{_libdir}/asterisk/modules/format_ilbc.so
%{_libdir}/asterisk/modules/format_ogg_speex.so
%{_libdir}/asterisk/modules/format_ogg_opus.so
%{_libdir}/asterisk/modules/format_pcm.so
%{_libdir}/asterisk/modules/format_siren7.so
%{_libdir}/asterisk/modules/format_siren14.so
%{_libdir}/asterisk/modules/format_sln.so
%{_libdir}/asterisk/modules/format_vox.so
%{_libdir}/asterisk/modules/format_wav_gsm.so
%{_libdir}/asterisk/modules/format_wav.so
%{_libdir}/asterisk/modules/func_aes.so
%{_libdir}/asterisk/modules/func_base64.so
%{_libdir}/asterisk/modules/func_blacklist.so
%{_libdir}/asterisk/modules/func_callcompletion.so
%{_libdir}/asterisk/modules/func_callerid.so
%{_libdir}/asterisk/modules/func_cdr.so
%{_libdir}/asterisk/modules/func_channel.so
%{_libdir}/asterisk/modules/func_config.so
%{_libdir}/asterisk/modules/func_cut.so
%{_libdir}/asterisk/modules/func_db.so
%{_libdir}/asterisk/modules/func_devstate.so
%{_libdir}/asterisk/modules/func_dialgroup.so
%{_libdir}/asterisk/modules/func_dialplan.so
%{_libdir}/asterisk/modules/func_enum.so
%{_libdir}/asterisk/modules/func_env.so
%{_libdir}/asterisk/modules/func_evalexten.so
%{_libdir}/asterisk/modules/func_extstate.so
%{_libdir}/asterisk/modules/func_frame_trace.so
%{_libdir}/asterisk/modules/func_global.so
%{_libdir}/asterisk/modules/func_groupcount.so
%{_libdir}/asterisk/modules/func_iconv.so
%{_libdir}/asterisk/modules/func_lock.so
%{_libdir}/asterisk/modules/func_logic.so
%{_libdir}/asterisk/modules/func_math.so
%{_libdir}/asterisk/modules/func_md5.so
%{_libdir}/asterisk/modules/func_module.so
%{_libdir}/asterisk/modules/func_pitchshift.so
%{_libdir}/asterisk/modules/func_rand.so
%{_libdir}/asterisk/modules/func_realtime.so
%{_libdir}/asterisk/modules/func_sha1.so
%{_libdir}/asterisk/modules/func_shell.so
%{_libdir}/asterisk/modules/func_sprintf.so
%{_libdir}/asterisk/modules/func_speex.so
%{_libdir}/asterisk/modules/func_srv.so
%{_libdir}/asterisk/modules/func_strings.so
%{_libdir}/asterisk/modules/func_sysinfo.so
%{_libdir}/asterisk/modules/func_timeout.so
%{_libdir}/asterisk/modules/func_uri.so
%{_libdir}/asterisk/modules/func_version.so
%{_libdir}/asterisk/modules/func_vmcount.so
%{_libdir}/asterisk/modules/func_volume.so
%{_libdir}/asterisk/modules/pbx_ael.so
%{_libdir}/asterisk/modules/pbx_config.so
%{_libdir}/asterisk/modules/pbx_dundi.so
%{_libdir}/asterisk/modules/pbx_loopback.so
%{_libdir}/asterisk/modules/pbx_lua.so
%{_libdir}/asterisk/modules/pbx_realtime.so
%{_libdir}/asterisk/modules/pbx_spool.so
%{_libdir}/asterisk/modules/res_adsi.so
%{_libdir}/asterisk/modules/res_ael_share.so
%{_libdir}/asterisk/modules/res_agi.so
%{_libdir}/asterisk/modules/res_audiosocket.so
%{_libdir}/asterisk/modules/res_calendar.so
%{_libdir}/asterisk/modules/res_calendar_caldav.so
%{_libdir}/asterisk/modules/res_calendar_ews.so
%{_libdir}/asterisk/modules/res_calendar_exchange.so
%{_libdir}/asterisk/modules/res_calendar_icalendar.so
%{_libdir}/asterisk/modules/res_chan_stats.so
%{_libdir}/asterisk/modules/res_clialiases.so
%{_libdir}/asterisk/modules/res_clioriginate.so
%{_libdir}/asterisk/modules/res_convert.so
%{_libdir}/asterisk/modules/res_crypto.so
%{_libdir}/asterisk/modules/res_endpoint_stats.so
%{_libdir}/asterisk/modules/res_fax.so
%{_libdir}/asterisk/modules/res_http_media_cache.so
%{_libdir}/asterisk/modules/res_format_attr_celt.so
%{_libdir}/asterisk/modules/res_format_attr_ilbc.so
%{_libdir}/asterisk/modules/res_format_attr_silk.so
%{_libdir}/asterisk/modules/res_format_attr_siren14.so
%{_libdir}/asterisk/modules/res_format_attr_siren7.so
%{_libdir}/asterisk/modules/res_format_attr_h263.so
%{_libdir}/asterisk/modules/res_format_attr_h264.so
%{_libdir}/asterisk/modules/res_format_attr_g729.so
%{_libdir}/asterisk/modules/res_limit.so
%{_libdir}/asterisk/modules/res_monitor.so
%{_libdir}/asterisk/modules/res_musiconhold.so
%{_libdir}/asterisk/modules/res_mutestream.so
%{_libdir}/asterisk/modules/res_phoneprov.so
%{_libdir}/asterisk/modules/res_prometheus.so
%{_libdir}/asterisk/modules/res_realtime.so
%{_libdir}/asterisk/modules/res_rtp_asterisk.so
%{_libdir}/asterisk/modules/res_rtp_multicast.so
%{_libdir}/asterisk/modules/res_security_log.so
%{_libdir}/asterisk/modules/res_smdi.so
%{_libdir}/asterisk/modules/res_speech.so
%{_libdir}/asterisk/modules/res_stun_monitor.so
%{_libdir}/asterisk/modules/res_timing_pthread.so
%{_libdir}/asterisk/modules/res_pktccops.so
%{_libdir}/asterisk/modules/res_config_ldap.so
%{_libdir}/asterisk/modules/res_fax_spandsp.so
%{_libdir}/asterisk/modules/func_jitterbuffer.so
%{_libdir}/asterisk/modules/func_presencestate.so
%{_libdir}/asterisk/modules/func_hangupcause.so
%{_libdir}/asterisk/modules/func_export.so
%{_libdir}/asterisk/modules/res_config_sqlite3.so
%{_libdir}/asterisk/modules/res_http_websocket.so
%{_libdir}/asterisk/modules/res_xmpp.so
%{_libdir}/asterisk/modules/res_mwi_devstate.so
%{_libdir}/asterisk/modules/res_srtp.so
%{_libdir}/asterisk/modules/app_agent_pool.so
%{_libdir}/asterisk/modules/app_bridgewait.so
%{_libdir}/asterisk/modules/app_stasis.so
%{_libdir}/asterisk/modules/bridge_builtin_interval_features.so
%{_libdir}/asterisk/modules/bridge_holding.so
%{_libdir}/asterisk/modules/bridge_native_rtp.so
%{_libdir}/asterisk/modules/chan_motif.so
%{_libdir}/asterisk/modules/chan_bridge_media.so
%{_libdir}/asterisk/modules/chan_pjsip.so
%{_libdir}/asterisk/modules/func_pjsip_endpoint.so
%{_libdir}/asterisk/modules/res_ari.so
%{_libdir}/asterisk/modules/res_aeap.so
%{_libdir}/asterisk/modules/res_speech_aeap.so
%{_libdir}/asterisk/modules/res_ari_applications.so
%{_libdir}/asterisk/modules/res_ari_asterisk.so
%{_libdir}/asterisk/modules/res_ari_bridges.so
%{_libdir}/asterisk/modules/res_ari_channels.so
%{_libdir}/asterisk/modules/res_ari_device_states.so
%{_libdir}/asterisk/modules/res_ari_endpoints.so
%{_libdir}/asterisk/modules/res_ari_events.so
%{_libdir}/asterisk/modules/res_ari_model.so
%{_libdir}/asterisk/modules/res_ari_playbacks.so
%{_libdir}/asterisk/modules/res_ari_recordings.so
%{_libdir}/asterisk/modules/res_ari_sounds.so
%{_libdir}/asterisk/modules/res_format_attr_opus.so
%{_libdir}/asterisk/modules/res_parking.so
%{_libdir}/asterisk/modules/res_pjsip.so
%{_libdir}/asterisk/modules/res_pjsip_acl.so
%{_libdir}/asterisk/modules/res_pjsip_aoc.so
%{_libdir}/asterisk/modules/res_pjsip_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_caller_id.so
%{_libdir}/asterisk/modules/res_pjsip_diversion.so
%{_libdir}/asterisk/modules/res_pjsip_dtmf_info.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_anonymous.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_ip.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_user.so
%{_libdir}/asterisk/modules/res_pjsip_exten_state.so
%{_libdir}/asterisk/modules/res_pjsip_header_funcs.so
%{_libdir}/asterisk/modules/res_pjsip_logger.so
%{_libdir}/asterisk/modules/res_pjsip_messaging.so
%{_libdir}/asterisk/modules/res_pjsip_mwi.so
%{_libdir}/asterisk/modules/res_pjsip_nat.so
%{_libdir}/asterisk/modules/res_pjsip_notify.so
%{_libdir}/asterisk/modules/res_pjsip_one_touch_record_info.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_registration.so
#%%{_libdir}/asterisk/modules/res_pjsip_pidf.so
%{_libdir}/asterisk/modules/res_pjsip_pubsub.so
%{_libdir}/asterisk/modules/res_pjsip_refer.so
%{_libdir}/asterisk/modules/res_pjsip_registrar.so
%{_libdir}/asterisk/modules/res_pjsip_rfc3326.so
%{_libdir}/asterisk/modules/res_pjsip_rfc3329.so
%{_libdir}/asterisk/modules/res_pjsip_sdp_rtp.so
%{_libdir}/asterisk/modules/res_pjsip_session.so
%{_libdir}/asterisk/modules/res_pjsip_stir_shaken.so
%{_libdir}/asterisk/modules/res_pjsip_t38.so
%{_libdir}/asterisk/modules/res_pjsip_transport_websocket.so
%{_libdir}/asterisk/modules/res_resolver_unbound.so
%{_libdir}/asterisk/modules/res_sorcery_astdb.so
%{_libdir}/asterisk/modules/res_sorcery_memory_cache.so
%{_libdir}/asterisk/modules/res_sorcery_config.so
%{_libdir}/asterisk/modules/res_sorcery_memory.so
%{_libdir}/asterisk/modules/res_sorcery_realtime.so
%{_libdir}/asterisk/modules/res_stasis.so
%{_libdir}/asterisk/modules/res_stasis_answer.so
%{_libdir}/asterisk/modules/res_stasis_device_state.so
%{_libdir}/asterisk/modules/res_stasis_playback.so
%{_libdir}/asterisk/modules/res_stasis_recording.so
%{_libdir}/asterisk/modules/res_stasis_snoop.so
%{_libdir}/asterisk/modules/res_statsd.so
%{_libdir}/asterisk/modules/res_stir_shaken.so
%{_libdir}/asterisk/modules/res_pjsip_mwi_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_eyebeam_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_xpidf_body_generator.so
%{_libdir}/asterisk/modules/func_sorcery.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_digium_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_send_to_voicemail.so
%{_libdir}/asterisk/modules/func_talkdetect.so
%{_libdir}/asterisk/modules/res_pjsip_dialog_info_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_phoneprov_provider.so
%{_libdir}/asterisk/modules/func_pjsip_aor.so
%{_libdir}/asterisk/modules/func_pjsip_contact.so
%{_libdir}/asterisk/modules/res_pjsip_config_wizard.so
#%%{_libdir}/asterisk/modules/res_pjsip_keepalive.so
#%%{_libdir}/asterisk/modules/res_pjsip_transport_management.so
%{_libdir}/asterisk/modules/res_pjsip_sips_contact.so
%{_libdir}/asterisk/modules/func_holdintercept.so
%{_libdir}/asterisk/modules/res_format_attr_vp8.so
%{_libdir}/asterisk/modules/res_odbc_transaction.so
%{_libdir}/asterisk/modules/res_pjproject.so
%{_libdir}/asterisk/modules/res_pjsip_history.so
%{_libdir}/asterisk/modules/res_pjsip_empty_info.so

%{_libdir}/asterisk/modules/app_sf.so
%{_libdir}/asterisk/modules/func_json.so

%{_libdir}/asterisk/modules/app_stream_echo.so
#%%{_libdir}/asterisk/modules/res_sdp_translator_pjmedia.so
%{_libdir}/asterisk/modules/app_mf.so
%{_libdir}/asterisk/modules/func_frame_drop.so
%{_libdir}/asterisk/modules/func_sayfiles.so
%{_libdir}/asterisk/modules/func_scramble.so
%{_libdir}/asterisk/modules/res_tonedetect.so

%{_libdir}/libasteriskpj.so
%{_libdir}/libasteriskpj.so.2

%{_sbindir}/asterisk
%{_sbindir}/rasterisk
%{_sbindir}/safe_asterisk
%{_sbindir}/astcanary
%{_sbindir}/astgenkey
%{_sbindir}/astdb2bdb
%{_sbindir}/astdb2sqlite3
%{_sbindir}/astversion

%{?_without_newt:%if 0}
%{!?_without_newt:%if 1}
#%%{_sbindir}/astman
%endif
%{_sbindir}/autosupport
%{_libdir}/asterisk/modules/app_jack.so
%{_libdir}/asterisk/modules/cdr_radius.so
%{_libdir}/asterisk/modules/cel_radius.so
%{_libdir}/asterisk/modules/chan_console.so
#%%{_libdir}/asterisk/modules/res_calendar_caldav.so
#%%{_libdir}/asterisk/modules/res_calendar_ews.so
#%%{_libdir}/asterisk/modules/res_calendar_exchange.so
#%%{_libdir}/asterisk/modules/res_calendar_icalendar.so
%{_libdir}/asterisk/modules/res_config_sqlite.so
%{_libdir}/asterisk/modules/res_timing_timerfd.so
%{_libdir}/libasteriskssl.so.1
%{_libdir}/libasteriskssl.so
#%%{_libdir}/asterisk/modules/res_ari_mailboxes.so
#%%{_libdir}/asterisk/modules/res_pjsip_multihomed.so
%{_libdir}/asterisk/modules/res_pjsip_path.so
%{_libdir}/asterisk/modules/func_periodic_hook.so
%{_libdir}/asterisk/modules/res_hep.so
%{_libdir}/asterisk/modules/res_hep_pjsip.so
%{_libdir}/asterisk/modules/res_hep_rtcp.so
%{_libdir}/asterisk/modules/res_manager_devicestate.so
%{_libdir}/asterisk/modules/res_manager_presencestate.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_publish.so
%{_libdir}/asterisk/modules/res_pjsip_publish_asterisk.so
%{_libdir}/asterisk/modules/res_pjsip_dlg_options.so

%{_sysconfdir}/asterisk/say.conf

%attr(0775,asterisk,asterisk) %dir %{logdir}/asterisk
%attr(0775,asterisk,asterisk) %dir %{logdir}/asterisk/cdr-csv
%attr(0775,asterisk,asterisk) %dir %{logdir}/asterisk/cdr-custom


%config %{_sysconfdir}/logrotate.d/asterisk

%attr(0775,asterisk,asterisk) %dir /var/run/asterisk

%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/agi-bin
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/documentation
%attr(0644,asterisk,asterisk)      /var/lib/asterisk/documentation/*
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/images
%attr(0644,asterisk,asterisk)      /var/lib/asterisk/images/*
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/keys
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/licenses
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/phoneprov
%attr(0644,asterisk,asterisk)      /var/lib/asterisk/phoneprov/*
%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/static-http
%attr(0644,asterisk,asterisk)      /var/lib/asterisk/static-http/*

%attr(0755,asterisk,asterisk) %dir /var/lib/digium
%attr(0755,asterisk,asterisk) %dir /var/lib/digium/licenses

%attr(0755,asterisk,asterisk) %dir /var/lib/asterisk/rest-api
%attr(0644,asterisk,asterisk)      /var/lib/asterisk/rest-api/*

%attr(0755,asterisk,asterisk)      /var/lib/asterisk/scripts/*

%attr(0775,asterisk,asterisk) %dir /var/spool/asterisk
%attr(0775,asterisk,asterisk) %dir /var/spool/asterisk/meetme
%attr(0775,asterisk,asterisk) %dir /var/spool/asterisk/system
%attr(0775,asterisk,asterisk) %dir /var/spool/asterisk/tmp
%attr(0775,asterisk,asterisk) %dir /var/spool/asterisk/voicemail

#
#  Alsa Subpackage
#
%{?_without_alsa:%if 0}
%{!?_without_alsa:%if 1}
%files alsa
%defattr(-, root, root)
%{_libdir}/asterisk/modules/chan_alsa.so
%endif

#
#  snmp Subpackage
#
%{?_without_snmp:%if 0}
%{!?_without_snmp:%if 1}
%files snmp
%defattr(-, root, root)
%{_libdir}/asterisk/modules/res_snmp.so
%endif

#
#  pgsql Subpackage
#
%{?_without_pgsql:%if 0}
%{!?_without_pgsql:%if 1}
%files pgsql
%defattr(-, root, root)
%{_libdir}/asterisk/modules/res_config_pgsql.so
%{_libdir}/asterisk/modules/cdr_pgsql.so
%{_libdir}/asterisk/modules/cel_pgsql.so
%endif

#
#  tds Subpackage
#
%{?_without_tds:%if 0}
%{!?_without_tds:%if 1}
%files tds
%defattr(-, root, root)
%{_libdir}/asterisk/modules/cdr_tds.so
%{_libdir}/asterisk/modules/cel_tds.so
%endif

#
#  mISDN Subpackage
#
%if %{with misdn}
%files misdn
%defattr(-, root, root)
%{_libdir}/asterisk/modules/chan_misdn.so
%endif

#
#  dahdi Subpackage
#
%{?_without_dahdi:%if 0}
%{!?_without_dahdi:%if 1}
%files dahdi
%defattr(-, root, root)
%{_libdir}/asterisk/modules/app_dahdiras.so
%{_libdir}/asterisk/modules/app_flash.so
%{_libdir}/asterisk/modules/app_meetme.so
%{_libdir}/asterisk/modules/app_page.so
%{_libdir}/asterisk/modules/chan_dahdi.so
%{_libdir}/asterisk/modules/codec_dahdi.so
%{_libdir}/asterisk/modules/res_timing_dahdi.so
%{_datadir}/dahdi/span_config.d/40-asterisk
%endif

#
#  Configs Subpackage
#
%files configs
%defattr(-, asterisk, asterisk)
%attr(0664,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/*

#
#  cURL Subpackage
#
%{?_without_curl:%if 0}
%{!?_without_curl:%if 1}
%files curl
%defattr(-, root, root)
%{_libdir}/asterisk/modules/func_curl.so
%{_libdir}/asterisk/modules/res_config_curl.so
%{_libdir}/asterisk/modules/res_curl.so
%endif

#
#  Development Subpackage
#
%files devel
%defattr(-, root, root)
%{_includedir}/asterisk.h
%{_includedir}/asterisk/*

#
#  Documentation Subpackage
#
%files doc
%defattr(-, root, root)

#
#  Manual Pages
#
%{_mandir}/man8/asterisk.8.gz
%{_mandir}/man8/astgenkey.8.gz
%{_mandir}/man8/autosupport.8.gz
%{_mandir}/man8/safe_asterisk.8.gz
%{_mandir}/man8/astdb2bdb.8.gz
%{_mandir}/man8/astdb2sqlite3.8.gz

#
#  Ogg-Vorbis Subpackage
#
%{?_without_ogg:%if 0}
%{!?_without_ogg:%if 1}
%files ogg
%defattr(-, root, root)
%{_libdir}/asterisk/modules/format_ogg_vorbis.so
%endif

#
#  Speex Subpackage
#
%{?_without_speex:%if 0}
%{!?_without_speex:%if 1}
%files speex
%defattr(-, root, root)
%{_libdir}/asterisk/modules/codec_speex.so
%endif

#
#  resample Subpackage
#
%files resample
%defattr(-, root, root)
%{_libdir}/asterisk/modules/codec_resample.so

#
#  unixODBC Subpackage
#
%{?_without_odbc:%if 0}
%{!?_without_odbc:%if 1}
%files odbc
%defattr(-, root, root)
%{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%{_libdir}/asterisk/modules/cdr_odbc.so
%{_libdir}/asterisk/modules/cel_odbc.so
%{_libdir}/asterisk/modules/func_odbc.so
%{_libdir}/asterisk/modules/res_config_odbc.so
%{_libdir}/asterisk/modules/res_odbc.so
%endif

#
#  sqlite3 Subpackage
#
%{?_without_sqlite3:%if 0}
%{!?_without_sqlite3:%if 1}
%files sqlite3
%defattr(-, root, root)
%{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%endif

#
#  voicemail file storage Subpackage
#
%files voicemail
%defattr(-, root, root)
%{_libdir}/asterisk/modules/app_voicemail.so

#
#  voicemail ODBC storage Subpackage
#
%{?_without_voicemail_odbcstorage:%if 0}
%{!?_without_voicemail_odbcstorage:%if 1}
%files voicemail-odbcstorage
%defattr(-, root, root)
%{_libdir}/asterisk/modules/app_voicemail_odbc.so
%endif

#
#  voicemail IMAP storage Subpackage
#
%{?_without_voicemail_imapstorage:%if 0}
%{!?_without_voicemail_imapstorage:%if 1}
%files voicemail-imapstorage
%defattr(-, root, root)
%{_libdir}/asterisk/modules/app_voicemail_imap.so
%endif

%files addons
%defattr(-, root, root)

%files addons-core
%defattr(-, root, root)
%{_libdir}/asterisk/modules/format_mp3.so

%{?_without_mysql:%if 0}
%{!?_without_mysql:%if 1}
%files addons-mysql
%{_libdir}/asterisk/modules/app_mysql.so
%{_libdir}/asterisk/modules/cdr_mysql.so
%{_libdir}/asterisk/modules/res_config_mysql.so
%endif

%{?_without_bluetooth:%if 0}
%{!?_without_bluetooth:%if 1}
%files addons-bluetooth
%{_libdir}/asterisk/modules/chan_mobile.so
%endif

%{?_without_ooh323:%if 0}
%{!?_without_ooh323:%if 1}
%files addons-ooh323
%{_libdir}/asterisk/modules/chan_ooh323.so
%endif

%changelog
* Fri Mar 10 2023 Franck Danard <fdanard@sangoma.com> - 18.17.0.1
- Update to upstream 18.17.0

* Tue Feb 21 2023 Franck Danard <fdanard@sangoma.com> - 18.16.0.2
- Fixe https://issues.freepbx.org/browse/FREEI-5616

* Thu Jan 12 2023 Franck Danard <fdanard@sangoma.com> - 18.16.0.1
- Update to upstream 18.16.0

* Fri Dec 02 2022 Franck Danard <fdanard@sangoma.com> - 18.15.1-1
- Update to upstream 18.15.1

* Mon Nov 07 2022 Franck Danard <fdanard@sangoma.com> - 18.15.0-1
- Update to upstream 18.15.0

* Fri Aug 19 2022 Franck Danard <fdanard@sangoma.com> - 18.14.0-1
- Update to upstream 18.14.0

* Fri Jun 24 2022 Franck Danard <fdanard@sangoma.com> - 18.13.0-1
- Update to upstream 18.13.0

* Fri May 20 2022 Franck Danard <fdanard@sangoma.com> - 18.12.1-1
- Fixe res_pjsip_transport_websocket 18.12.1

* Thu May 12 2022 Franck Danard <fdanard@sangoma.com> - 18.12.0-1
- Update to upstream 18.12.0

* Wed Apr 27 2022 Franck Danard <fdanard@sangoma.com> - 18.11.3-1
- Update to upstream 18.11.3

* Tue Apr 19 2022 Franck Danard <fdanard@sangoma.com> - 18.11.2-1
- Update to upstream 18.11.2

* Mon Apr 04 2022 Franck Danard <fdanard@sangoma.com> - 18.11.1-1
- Update to upstream 18.11.1

* Thu Mar 24 2022 Franck Danard <fdanard@sangoma.com> - 18.11.0-1
- Update to upstream 18.11.0

* Mon Mar 07 2022 Franck Danard <fdanard@sangoma.com> - 18.10.1-1
- Security release 18.10.1

* Thu Feb 17 2022 Franck Danard <fdanard@sangoma.com> - 18.10.0.1
- Update to upstream 18.10.0 release

* Wed Dec 22 2021 Franck Danard <fdanard@sangoma.com> - 18.9.0.1
- Update to upstream 18.9.0 release

* Mon Aug 23 2021 Franck Danard <fdanard@sangoma.com> - 18.6.0.1
- Update to upstream 18.6.0 release, FREEI-3796

* Fri Apr 09 2021 Franck Danard <fdanard@sangoma.com> - 18.3.0.1
- Update to upstream 18.5.0 release, FREEPBX-22499

* Fri Apr 09 2021 Franck Danard <fdanard@sangoma.com> - 18.3.0.1
- Update to upstream 18.3.0 release https://issues.asterisk.org/jira/browse/ASTERISK-28369

* Mon Mar 08 2021 Franck Danard <fdanard@sangoma.com> - 18.2.2-1
- Update to upstream 18.2.2 release for security and bug fixes

* Tue Dec 22 2020 Walter Moon <wmoon@sangoma.com> - 18.1.1-1
- Update to 18.1.1 release for bug fixes

* Tue Nov 24 2020 Franck Danard <fdanard@sangoma.com> - 18.1.0-1
- Update to 18.1.0 release for bug fixes

* Tue Oct 27 2020 Walter Moon <wmoon@sangoma.com> - 18.0.0-1
- Release of 18.0.0
