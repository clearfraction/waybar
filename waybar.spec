Name     : waybar
Version  : 0.10.0
Release  : 1
URL      : https://github.com/Alexays/Waybar
Source0  : https://github.com/Alexays/Waybar/archive/refs/tags/%{version}.tar.gz
Summary  : Customizable Wayland bar for Sway and Wlroots based compositors
Group    : Development/Tools
License  : MIT
Requires : sway
BuildRequires :  meson cmake
BuildRequires :  scdoc-dev
BuildRequires :  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires :  pkgconfig(fmt) >= 7.0.0
BuildRequires :  pkgconfig(gdk-pixbuf-2.0)
BuildRequires :  pkgconfig(gio-unix-2.0)
BuildRequires :  pkgconfig(gtkmm-3.0)
BuildRequires :  pkgconfig(jsoncpp)
BuildRequires :  pkgconfig(libevdev)
BuildRequires :  pkgconfig(libinput)
BuildRequires :  pkgconfig(libnl-3.0)
BuildRequires :  pkgconfig(libnl-genl-3.0)
BuildRequires :  pkgconfig(libpulse)
BuildRequires :  pkgconfig(libudev)
BuildRequires :  pkgconfig(sigc++-2.0)
BuildRequires :  pkgconfig(upower-glib)
BuildRequires :  pkgconfig(wayland-client)
BuildRequires :  pkgconfig(wayland-cursor)
BuildRequires :  pkgconfig(wayland-protocols)
BuildRequires :  pkgconfig(xkbregistry)
BuildRequires :  wayland-protocols-dev


%description
Customizable Wayland bar for Sway and Wlroots based compositors

%prep
%setup -q -n Waybar-%{version}


# fix resources path
sed -i 's|"./resources/"|"./resources/", "/opt/3rd-party/bundles/clearfraction/usr/share/xdg/waybar"|g' src/config.cpp

%build
unset http_proxy https_proxy no_proxy
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -Ofast -fno-lto "
export FCFLAGS="$FFLAGS -Ofast -fno-lto "
export FFLAGS="$FFLAGS -Ofast -fno-lto "
export CXXFLAGS="$CXXFLAGS -Ofast -fno-lto "
rpm -ivh --nodeps https://download.clearlinux.org/releases/37560/clear/x86_64/os/Packages/spdlog-1.10.0-11.x86_64.rpm https://download.clearlinux.org/releases/37560/clear/x86_64/os/Packages/spdlog-dev-1.10.0-11.x86_64.rpm https://download.clearlinux.org/releases/37560/clear/x86_64/os/Packages/spdlog-lib-1.10.0-11.x86_64.rpm
CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" meson -Dsndio=disabled -Dcpp_std=c++17 -Dcava=disabled -Dtests=disabled -Dman-pages=disabled --libdir=lib64 --prefix=/usr --buildtype=plain   builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install
mkdir -p %{buildroot}/{usr/share/xdg/waybar,usr/lib64}
mv resources/* %{buildroot}/usr/share/xdg/waybar
mv /usr/lib64/libspdlog.so* %{buildroot}/usr/lib64
rm -rf %{buildroot}{/usr/include,/usr/lib64/pkgconfig}


%files
%defattr(-,root,root,-)
/usr/bin/waybar
/usr/lib/systemd/user/waybar.service
/usr/lib64/libspdlog*
/usr/lib64/libjsoncpp*
/usr/share/xdg/waybar
