%define _name netcdf_f
%define _version 4.4.5
%define _compiler gnu
%define _compiler_version 6.5.0

%if "%{_compiler}" == "gnu"
	%define _compiler_desc gcc-%{_compiler_version}
	%define _cc "gcc" 
	%define _cxx "c++"
	%define _f77 "gfortran"
	%define _fc "gfortran"
%endif

%if "%{_compiler}" == "intel"
	%define _compiler_desc intel-2013
	%define _cc icc
	%define _cxx icpc
	%define _f77 ifort
	%define _fc ifort
%endif

Name:           anm-netcdf-f
Version:       	%{_version}
Release:        %{_compiler_version}.2%{?dist}
Summary:        anm-netcdf-f
BuildRequires:  zlib-devel >= 1.2.5
BuildRequires:  libcurl-devel
BuildRequires:  anm-hdf5 >= 1.8.8
BuildRequires:  anm-netcdf
Requires:       anm-netcdf
Requires:       environment-modules
AutoReqProv:    no

Group:          Miscellanous
License:        GPL
Source0:        https://github.com/Unidata/netcdf-fortran/archive/v%{_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%define _install_path /opt/tools/libraries/netcdf/%{_version}-f-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/netcdf-f-%{_version}-%{_compiler_desc}

%description
anm-netcdf-f

%prep
%setup -q -n netcdf-fortran-%{_version}


%build
export CFLAGS="-L$hdf5_LIB -I$hdf5_INC -L$netcdf_LIB -I$netcdf_INC"
export CXXFLAGS="-L$hdf5_LIB -I$hdf5_INC -L$netcdf_LIB -I$netcdf_INC"
export FCFLAGS="-L$hdf5_LIB -I$hdf5_INC -L$netcdf_LIB -I$netcdf_INC"
export CPPFLAGS="-I$hdf5_INC -I$netcdf_INC"
export LDFLAGS="-L$hdf5_LIB -L$netcdf_LIB"

./configure --prefix=%{_install_path} \
    --enable-shared \
    --enable-netcdf-4 \
    --enable-dap \
    --enable-ncgen4 \
    --with-pic \
    --disable-doxygen \
    --disable-static 
make clean
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install

install -d -m 755 $RPM_BUILD_ROOT/etc/modulefiles/libraries/
cat > $RPM_BUILD_ROOT%{_module_path} <<EOF
#%Module1.0
prepend-path PATH               %{_install_path}/bin
prepend-path LD_LIBRARY_PATH    %{_install_path}/lib
prepend-path INCLUDE            %{_install_path}/include
prepend-path MANPATH            %{_install_path}/share/man

setenv          %{_name}_DIR        %{_install_path}
setenv          %{_name}_LIB        %{_install_path}/lib
setenv          %{_name}_BIN        %{_install_path}/bin
setenv          %{_name}_INC        %{_install_path}/include
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_install_path}/
%{_module_path}
