# Run tests in check section
# disable for bootstrapping
%bcond_with check
#%global _unpackaged_files_terminate_build 0
%global with_debug 0

%if 0%{?with_debug}
%global debug_package   %{nil}
%endif

%global sname deepin-api

# out of memory on armv7hl
%ifarch %{arm}
%global _smp_mflags -j1
%endif

%global goipath  pkg.deepin.io/dde/api
%global forgeurl https://github.com/linuxdeepin/dde-api
%global tag      %{version}

Name:           dde-api
Version:        5.4.6
Release:        2
Summary:        Go-lang bingding for dde-daemon
License:        GPLv3+
URL:            https://shuttle.corp.deepin.com/cache/tasks/19177/unstable-amd64/
Source0:        %{name}-%{version}.orig.tar.xz
Source1:        vendor.tar.gz

BuildRequires:  libcanberra-devel
BuildRequires:  deepin-gettext-tools
BuildRequires:  librsvg2-devel
BuildRequires:  sqlite-devel
#BuildRequires:  go-compiler
BuildRequires:  golang golang-devel
BuildRequires:  gdk-pixbuf-xlib
BuildRequires:  kf5-kwayland-devel
BuildRequires:  poppler-glib
BuildRequires:  poppler-glib-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  alsa-lib
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libgudev-devel
%{?systemd_requires}
Requires:       deepin-desktop-base
Requires:       rfkill
Requires(pre):  shadow-utils

%description
%{summary}.

%package -n %{name}-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}-devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%forgeautosetup -p1 -n %{name}-%{version}

sed -i 's|/usr/lib|%{_libexecdir}|' misc/*services/*.service \
    misc/systemd/system/deepin-shutdown-sound.service \
    lunar-calendar/main.go \
    theme_thumb/gtk/gtk.go \
    thumbnails/gtk/gtk.go

sed -i 's|PREFIX}${libdir|LIBDIR|; s|libdir|LIBDIR|' \
    Makefile adjust-grub-theme/main.go
tar -xf %{SOURCE1}

%build
go env -w GO111MODULE=auto
export GOPATH=%{_builddir}/%{name}-%{version}/vendor:$GOPATH
%make_build

%install
for file in $(find . -iname "*.go" -o -iname "*.c" -o -iname "*.h" -o -iname "*.s"); do
    install -d -p %{buildroot}/%{gopath}/src/%{goipath}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{goipath}/$file
    echo "%{gopath}/src/%{goipath}/$file" >> devel.file-list
done
%make_install SYSTEMD_SERVICE_DIR="%{_unitdir}" LIBDIR="%{_libexecdir}"
# HOME directory for user deepin-sound-player
mkdir -p %{buildroot}%{_sharedstatedir}/deepin-sound-player

%pre
getent group deepin-sound-player >/dev/null || groupadd -r deepin-sound-player
getent passwd deepin-sound-player >/dev/null || \
    useradd -r -g deepin-sound-player -d %{_sharedstatedir}/deepin-sound-player\
    -s /sbin/nologin \
    -c "User of com.deepin.api.SoundThemePlayer.service" deepin-sound-player
exit 0

%post
%systemd_post deepin-shutdown-sound.service

%preun
%systemd_preun deepin-shutdown-sound.service

%postun
%systemd_postun_with_restart deepin-shutdown-sound.service

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-open
%{_libexecdir}/%{sname}/
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*
%{_datadir}/dde-api/data/huangli.db
%{_datadir}/dde-api/data/huangli.version
%{_datadir}/dde-api/data/pkg_depends
%{_datadir}/dde-api/data/grub-themes/
%{_datadir}/polkit-1/actions/com.deepin.api.locale-helper.policy
%{_datadir}/polkit-1/actions/com.deepin.api.device.unblock-bluetooth-devices.policy
%{_var}/lib/polkit-1/localauthority/10-vendor.d/com.deepin.api.device.pkla
%attr(-, deepin-sound-player, deepin-sound-player) %{_sharedstatedir}/deepin-sound-player

%files -n %{name}-devel -f devel.file-list

%changelog
* Wed Dec 21 2022 liweiganga <liweiganga@uniontech.com> - 5.4.6-2
- enable debuginfo for fix strip

* Mon Jul 18 2022 konglidong <konglidong@uniontech.com> - 5.4.6-1
- Update to 5.4.6

* Sat Jan 29 2022 liweiganga <liweiganga@uniontech.com> - 5.2.0-2
- fix build error.

* Thu Aug 26 2021 weidong <weidong@uniontech.com> - 5.2.0-1
- Update dde-api.

* Thu Mar 4 2021 weidong <weidong@uniontech.com> - 5.1.11.1-8
- Update license.

* Thu Feb 18 2021 panchenbo <panchenbo@uniontech.com> - 5.1.11.1-7
- fix build error
* Thu Sep 3 2020 weidong <weidong@uniontech.com> - 5.1.11.1-6
- fix source url in spec
* Wed Sep 2 2020 chenbo pan <panchenbo@uniontech.com> - 5.1.11.1-5
- remove dde-api-devel
* Wed Sep 2 2020 chenbo pan <panchenbo@uniontech.com> - 5.1.11.1-4
- remove install golang devel
* Tue Aug 18 2020 chenbo pan <panchenbo@uniontech.com> - 5.1.11.1-3
- remove golang devel
* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.1.11.1-2
- fix spec
* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.1.11.1-1
- Package init
