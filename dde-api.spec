%bcond_with check
%global goipath  pkg.deepin.io/lib

Name:           dde-api
Version:        5.2.0
Release:        3
Summary:        dde-api
License:        GPLv3
URL:            https://shuttle.corp.deepin.com/cache/tasks/19177/unstable-amd64/
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-fix-riscv64-support.patch
BuildRequires:  golang
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  deepin-gettext-tools

%define debug_package %{nil}

%description
dde-api

%prep
%setup
%patch0 -p1
go env -w GO111MODULE=auto

%build
make -C ./gir generator
make -C ./gir
cp -r ./gir/out/src/pkg.deepin.io/gir/ ./pkg.deepin.io

%install
install -d -p %{buildroot}/%{gopath}/src/
for file in $(find . -iname "*.go" -o -iname "*.c" -o -iname "*.h" -o -iname "*.s") ; do
    install -d -p %{buildroot}/%{gopath}/src/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/$file
    #echo "%{gopath}/src/$file" >> devel.file-list
done

make -C ./pkg.deepin.io/dde/api/ GOPATH=%{buildroot}/%{gopath}

install -d -p %{buildroot}/usr/lib/deepin-api
for file in $(ls ./pkg.deepin.io/dde/api/out/bin) ; do
    cp -pav ./pkg.deepin.io/dde/api/out/bin/$file %{buildroot}/usr/lib/deepin-api/$file
    echo "/usr/lib/deepin-api/$file" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/dbus-1/system.d/
for file in $(find ./pkg.deepin.io/dde/api/misc -iname "*.conf") ; do
    cp -pav $file %{buildroot}/usr/share/dbus-1/system.d/$(basename $file)
    echo "/usr/share/dbus-1/system.d/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/dbus-1/services/
for file in $(find ./pkg.deepin.io/dde/api/misc/services -iname "*.service") ; do
    cp -pav $file %{buildroot}/usr/share/dbus-1/services/$(basename $file)
    echo "/usr/share/dbus-1/services/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/dbus-1/system-services/
for file in $(find ./pkg.deepin.io/dde/api/misc/system-services -iname "*.service") ; do
    cp -pav $file %{buildroot}/usr/share/dbus-1/system-services/$(basename $file)
    echo "/usr/share/dbus-1/system-services/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/polkit-1/actions
for file in $(find ./pkg.deepin.io/dde/api/misc/polkit-action -iname "*.policy") ; do
    cp -pav $file %{buildroot}/usr/share/polkit-1/actions/$(basename $file)
    echo "/usr/share/polkit-1/actions/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/var/lib/polkit-1/localauthority/10-vendor.d
for file in $(find ./pkg.deepin.io/dde/api/misc/polkit-localauthority -iname "*.pkla") ; do
    cp -pav $file %{buildroot}/var/lib/polkit-1/localauthority/10-vendor.d/$(basename $file)
    echo "/var/lib/polkit-1/localauthority/10-vendor.d/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/dde-api
for file in $(find ./pkg.deepin.io/dde/api/misc/data) ; do
    cp -pav $file %{buildroot}/usr/share/dde-api/$(basename $file)
    echo "/usr/share/dde-api/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/lib/systemd/system/
for file in $(find ./pkg.deepin.io/dde/api/misc/systemd/system/ -iname "*.service") ; do
    cp -pav $file %{buildroot}/lib/systemd/system/$(basename $file)
    echo "/lib/systemd/system/$(basename $file)" >> devel.file-list
done

install -d -p %{buildroot}/usr/share/icons/hicolor
for file in $(find ./pkg.deepin.io/dde/api/misc/icons/) ; do
    cp -pav $file %{buildroot}/usr/share/icons/hicolor/$(basename $file)
    echo "/usr/share/icons/hicolor/$(basename $file)" >> devel.file-list
done
rm -rf %{buildroot}/%{gopath}

%files -f devel.file-list

%changelog
* Fri Jun 10 2022 misaka00251 <misaka00251@misakanet.cn> - 5.2.0-3
- Add patch to fix RISC-V support.

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
