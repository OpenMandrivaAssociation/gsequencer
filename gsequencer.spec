# Tests are useful only while updating the package
%bcond_with	check

%define	major	8
%define libname	%mklibname ags %{major}
%define devname	%mklibname -d ags

Summary:	 Audio processing engine
Name:	gsequencer
Version: 8.0.14
Release:	1
License:	GPLv3+ and AGPLv3+
Group:	Sound
Url:	 https://nongnu.org/gsequencer
Source0:	 https://github.com/gsequencer/gsequencer/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
BuildRequires:		chrpath
BuildRequires:		desktop-file-utils
BuildRequires:		docbook-style-xsl
BuildRequires:		gettext-devel
BuildRequires:		gstreamer1.0-plugins-base
BuildRequires:		gstreamer1.0-plugins-good
BuildRequires:		gtk-doc
BuildRequires:		libtool
BuildRequires:		python
BuildRequires:		xsltproc
%if %{with check}
BuildRequires:		cunit
BuildRequires:		x11-server-xvfb
%endif
BuildRequires:		ladspa-devel
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(cairo) >= 1.12.0
BuildRequires:		pkgconfig(dssi)
BuildRequires:		pkgconfig(fftw3)
BuildRequires:		pkgconfig(glib-2.0) >= 2.68.0
BuildRequires:		pkgconfig(gobject-introspection-1.0)
BuildRequires:		pkgconfig(gstreamer-1.0)
BuildRequires:		pkgconfig(gstreamer-app-1.0)
BuildRequires:		pkgconfig(gstreamer-video-1.0)
BuildRequires:		pkgconfig(gstreamer-audio-1.0)
BuildRequires:		pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:		pkgconfig(gtk4)
BuildRequires:		pkgconfig(gtk+-3.0)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(json-glib-1.0)
BuildRequires:		pkgconfig(libinstpatch-1.0)
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(libsoup-3.0)
BuildRequires:		pkgconfig(libxml-2.0) >= 2.8.0
BuildRequires:		pkgconfig(lv2)
BuildRequires:		pkgconfig(poppler-glib)
BuildRequires:		pkgconfig(samplerate)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(uuid) >= 1.0.1
BuildRequires:		pkgconfig(vst3sdk)
BuildRequires:		pkgconfig(vte-2.91-gtk4)
BuildRequires:		pkgconfig(webkit2gtk-4.1)
BuildRequires:		pkgconfig(x11)
Requires:	xml-common

%description
Advanced Gtk+ Sequencer audio processing engine is an audio sequencer
application supporting LADPSA, DSSI and Lv2 plugin format. It can output to
Pulseaudio server, JACK audio connection kit, ALSA, OSS4 and VST3.
You may add multiple sinks, mix different sources by producing sound with
different sequencers. Further it features a pattern and piano roll. Additional
there is a automation editor to automate ports.

%files -f %{name}.lang
%license COPYING
%{_docdir}/%{name}/
%{_bindir}/%{name}
%{_bindir}/midi2xml
%{_datadir}/%{name}/
%{_datadir}/xml/%{name}/
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/org.nongnu.%{name}.%{name}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/midi2xml.1*

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:  Advanced Gtk+ Sequencer library
Group:	System/Libraries
Conflicts:	%{name} < %{version}-%{release}

%description -n %{libname}
Advanced Gtk+ Sequencer audio processing engine is an audio sequencer
application supporting LADPSA, DSSI and Lv2 plugin format. It can output to
Pulseaudio server, JACK audio connection kit, ALSA, OSS4 and VST3.
This package contains the library files needed by %{name}.

%files -n %{libname}
%{_libdir}/libags.so.%{major}*
%{_libdir}/libags_thread.so.%{major}*
%{_libdir}/libags_server.so.%{major}*
%{_libdir}/libags_gui.so.%{major}*
%{_libdir}/libags_audio.so.%{major}*
%{_libdir}/libgsequencer.so.0*
%{_libdir}/girepository-1.0/*.typelib

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:  Advanced Gtk+ Sequencer library development files
Group:	Development/C++
Requires: %{libname} = %{version}-%{release}
Provides:	ags-devel = %{version}-%{release}
%rename	%{name}-devel

%description -n %{devname}
Advanced Gtk+ Sequencer library development files.

%files -n %{devname}
%{_includedir}/ags/
%{_libdir}/libags.so
%{_libdir}/libags_thread.so
%{_libdir}/libags_server.so
%{_libdir}/libags_gui.so
%{_libdir}/libags_audio.so
%{_libdir}/libgsequencer.so
%{_datadir}/gir-1.0/*.gir
%{_libdir}/pkgconfig/libags.pc
%{_libdir}/pkgconfig/libags_audio.pc
%{_libdir}/pkgconfig/libags_gui.pc
%{_libdir}/pkgconfig/libgsequencer.pc

#-----------------------------------------------------------------------------

%package -n gsequencer-devel-doc
Summary:  Advanced Gtk+ Sequencer library development documentation
Group:	Books/Computer books
BuildArch: noarch

%description -n gsequencer-devel-doc
Advanced Gtk+ Sequencer library development documentation.

%files -n gsequencer-devel-doc
%{_datadir}/gtk-doc/
%{_datadir}/doc/libags-audio-doc/

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
autoreconf -vfi
export CXXFLAGS="%{optflags} -fPIE"
export LDFLAGS="%{ldflags} -pie"
export CPPFLAGS='-DAGS_CSS_FILENAME=\"/usr/share/gsequencer/styles/ags.css\" -DAGS_ANIMATION_FILENAME=\"/usr/share/gsequencer/images/gsequencer-800x450.png\" -DAGS_LOGO_FILENAME=\"/usr/share/gsequencer/images/ags.png\" -DAGS_LICENSE_FILENAME=\"/usr/share/licenses/gsequencer/COPYING\" -DAGS_ONLINE_HELP_START_FILENAME=\"file:///usr/share/doc/gsequencer/html/index.html\"'
%configure HTMLHELP_XSL="/usr/share/sgml/docbook/xsl-stylesheets-1.79.2/htmlhelp/htmlhelp.xsl" \
						--disable-upstream-gtk-doc \
						--enable-introspection \
						--disable-oss \
						--disable-vst3 \
						--enable-vte \
						--enable-gtk-doc \
						--enable-gtk-doc-html \
						--with-poppler \
						--with-tooltips

%make_build
%make_build html
%make_build fix-local-html


%install
%make_install

%make_install install-compress-changelog
%make_install install-html-mkdir
%make_install install-html-mkdir-links
%make_install install-html

chrpath --delete %{buildroot}%{_bindir}/%{name}
chrpath --delete %{buildroot}%{_bindir}/midi2xml
chrpath --delete %{buildroot}%{_libdir}/libags.so*
chrpath --delete %{buildroot}%{_libdir}/libags_server.so*
chrpath --delete %{buildroot}%{_libdir}/libags_thread.so*
chrpath --delete %{buildroot}%{_libdir}/libags_gui.so*
chrpath --delete %{buildroot}%{_libdir}/libags_audio.so*
chrpath --delete %{buildroot}%{_libdir}/libgsequencer.so*


%find_lang %{name}


%if %{with check}
%check
xvfb-run --server-args="-screen 0 1920x1080x24" -a make check
%endif
