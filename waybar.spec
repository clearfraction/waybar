Name     : waybar
Version  : 0.9.13
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
BuildRequires :  pkgconfig(spdlog) >= 1.8.5
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
sed -i 's|"./resources/"|"./resources/", "/opt/3rd-party/bundles/clearfraction/usr/share/waybar"|g' src/config.cpp

%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -Ofast -ffat-lto-objects -flto=auto "
export FCFLAGS="$FFLAGS -Ofast -ffat-lto-objects -flto=auto "
export FFLAGS="$FFLAGS -Ofast -ffat-lto-objects -flto=auto "
export CXXFLAGS="$CXXFLAGS -Ofast -ffat-lto-objects -flto=auto "
CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" meson -Dsndio=disabled --libdir=lib64 --prefix=/usr --buildtype=plain   builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install
rm -rf %{buildroot}/usr/share/man
cp -r resources %{buildroot}/usr/share/waybar

%files
%defattr(-,root,root,-)
/usr/bin/waybar
/usr/lib/systemd/user/waybar.service
/usr/share/waybar
