%define _name cmake
%define _version 3.15.1
%define _compiler gnu
%define _compiler_version 6.5.0

%define _install_path /opt/tools/utilities/%{_name}/%{_version}
%define _module_path /etc/modulefiles/utilities/%{_name}-%{_version}

Name:           anm-%{_name}
Release:        1%{?dist}
Version:        %{_version}
Summary:        anm-%{_name}
BuildRequires:  openjpeg-devel
BuildRequires:  python-devel
BuildRequires:  numpy
Requires:       openjpeg
Requires:       numpy
Requires:       environment-modules
AutoReqProv:    no


Group:          Miscellanous
License:        GPL
Source0:        https://github.com/Kitware/CMake/releases/download/v3.15.1/cmake-3.15.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
anm-{%_name}

%prep
%setup -q -n -q -n cmake-%{_version}

%build
export CC=%{_cc} 
export CXX=${_cxx} 
export F77=%{_f77} 
export FC=%{_fc}
export LDFLAGS=%{_ldflags}

./configure --prefix=%{_install_path}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

install -d -m 755 $RPM_BUILD_ROOT/etc/modulefiles/libraries/
cat > $RPM_BUILD_ROOT%{_module_path} <<EOF
#%Module1.0
prepend-path PATH               %{_install_path}/bin
prepend-path LD_LIBRARY_PATH    %{_install_path}/lib
prepend-path INCLUDE            %{_install_path}/include
prepend-path PKG_CONFIG_PATH    %{_install_path}/lib/pkgconfig

setenv %{_name}_DIR             %{_install_path}
setenv %{_name}_INC             %{_install_path}/include
setenv %{_name}_LIB             %{_install_path}/lib
setenv %{_name}_BIN             %{_install_path}/bin
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_install_path}
%{_module_path}
