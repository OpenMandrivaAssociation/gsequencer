#global optflags %{optflags} -fuse-ld=gold

Name:     gsequencer
Version:  3.15.3
Release:  1
Summary:  Audio processing engine
License:  GPLv3+ and AGPLv3+ and GFDL-1.3+
Group:		Sound
URL:      http://nongnu.org/gsequencer
Source:   http://download.savannah.gnu.org/releases/gsequencer/3.15.x/%{name}-%{version}.tar.gz

BuildRequires:      make
BuildRequires:      libtool
BuildRequires:      chrpath
BuildRequires:      docbook-style-xsl
BuildRequires:      gettext-devel
BuildRequires:      gtk-doc
BuildRequires:      pkgconfig(uuid)
BuildRequires:      pkgconfig(libxml-2.0)
BuildRequires:      pkgconfig(libsoup-2.4)
BuildRequires:      pkgconfig(alsa)
BuildRequires:      pkgconfig(fftw3)
BuildRequires:      ladspa-devel
BuildRequires:      dssi-devel
BuildRequires:      lv2-devel
BuildRequires:      gstreamer1.0-plugins-base
BuildRequires:      gstreamer1.0-plugins-good
BuildRequires:      pkgconfig(jack)
BuildRequires:      pkgconfig(samplerate)
BuildRequires:      pkgconfig(sndfile)
BuildRequires:      pkgconfig(libinstpatch-1.0)
BuildRequires:      pkgconfig(gtk+-3.0)
BuildRequires:      pkgconfig(webkit2gtk-4.0)
BuildRequires:      pkgconfig(gstreamer-1.0)
BuildRequires:      pkgconfig(gstreamer-app-1.0)
BuildRequires:      pkgconfig(gstreamer-video-1.0)
BuildRequires:      pkgconfig(gstreamer-audio-1.0)
BuildRequires:      pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:      pkgconfig(gobject-introspection-1.0)
BuildRequires:      pkgconfig(libpulse)
BuildRequires:      pkgconfig(cunit)
BuildRequires:      desktop-file-utils
BuildRequires:      x11-server-xvfb
Requires:           xml-common

%description
Advanced Gtk+ Sequencer audio processing engine is an audio
sequencer application supporting LADPSA, DSSI and Lv2 plugin
format. It can output to Pulseaudio server, JACK audio connection
kit, ALSA and OSS4.

You may add multiple sinks, mix different sources by producing
sound with different sequencers. Further it features a pattern
and piano roll. Additional there is a automation editor to
automate ports.

%prep
%autosetup -N

%build
export CC=gcc
export CXX=g++
%undefine _strict_symbol_defs_build
autoreconf -fi
export CPPFLAGS='-DAGS_CSS_FILENAME=\"/usr/share/gsequencer/styles/ags.css\" -DAGS_ANIMATION_FILENAME=\"/usr/share/gsequencer/images/gsequencer-800x450.png\" -DAGS_LOGO_FILENAME=\"/usr/share/gsequencer/images/ags.png\" -DAGS_LICENSE_FILENAME=\"/usr/share/licenses/gsequencer/COPYING\" -DAGS_ONLINE_HELP_START_FILENAME=\"file:///usr/share/doc/gsequencer/html/index.html\"'
%configure HTMLHELP_XSL="/usr/share/sgml/docbook/xsl-stylesheets/htmlhelp/htmlhelp.xsl" --disable-upstream-gtk-doc --enable-introspection --disable-oss --enable-gtk-doc --enable-gtk-doc-html
%make_build
%make_build html
%make_build fix-local-html

%install
%make_install
%make_install install-compress-changelog
%make_install install-html-mkdir
%make_install install-html-mkdir-links
%make_install install-html
chrpath --delete %{buildroot}%{_bindir}/gsequencer
chrpath --delete %{buildroot}%{_bindir}/midi2xml
chrpath --delete %{buildroot}%{_libdir}/libags.so*
chrpath --delete %{buildroot}%{_libdir}/libags_server.so*
chrpath --delete %{buildroot}%{_libdir}/libags_thread.so*
chrpath --delete %{buildroot}%{_libdir}/libags_gui.so*
chrpath --delete %{buildroot}%{_libdir}/libags_audio.so*
chrpath --delete %{buildroot}%{_libdir}/libgsequencer.so*
find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/doc-base/
%find_lang %{name}

%check
xvfb-run --server-args="-screen 0 1920x1080x24" -a make check
desktop-file-validate %{buildroot}/%{_datadir}/applications/gsequencer.desktop

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%{_libdir}/libags.so.*
%{_libdir}/libags_thread.so.*
%{_libdir}/libags_server.so.*
%{_libdir}/libags_gui.so.*
%{_libdir}/libags_audio.so.*
%{_libdir}/libgsequencer.so.*
%{_libdir}/girepository-1.0
%{_bindir}/gsequencer
%{_bindir}/midi2xml
%{_mandir}/man1/gsequencer.1*
%{_mandir}/man1/midi2xml.1*
%{_datadir}/gsequencer/
%{_datadir}/xml/gsequencer/
%{_datadir}/icons/hicolor/*/apps/gsequencer.png
%{_datadir}/metainfo/
%{_datadir}/mime/packages/
%{_docdir}/gsequencer/
%{_datadir}/applications/gsequencer.desktop

%package devel
Summary:  Advanced Gtk+ Sequencer library development files
Requires: %{name}%{_isa} = %{version}-%{release}
%description devel
Advanced Gtk+ Sequencer library development files.

%files devel
%{_includedir}/ags/
%{_libdir}/libags.so
%{_libdir}/libags_thread.so
%{_libdir}/libags_server.so
%{_libdir}/libags_gui.so
%{_libdir}/libags_audio.so
%{_libdir}/libgsequencer.so
%{_datadir}/gir-1.0
%{_libdir}/pkgconfig/libags.pc
%{_libdir}/pkgconfig/libags_audio.pc
%{_libdir}/pkgconfig/libags_gui.pc
%{_libdir}/pkgconfig/libgsequencer.pc

%package -n gsequencer-devel-doc
Summary:  Advanced Gtk+ Sequencer library development documentation
BuildArch: noarch
%description -n gsequencer-devel-doc
Advanced Gtk+ Sequencer library development documentation.

%files -n gsequencer-devel-doc
%{_datadir}/gtk-doc/
%{_datadir}/doc/libags-audio-doc/
