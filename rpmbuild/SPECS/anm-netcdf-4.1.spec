%define _name netcdf
%define _compiler gnu

%if %{?_user_version:1}%{!?_user_version:0}
%define _version %{_user_version}
%else
%define _version 4.6.3
%endif

%if %{?_user_compiler_version:1}%{!?_user_compiler_version:0}
%define _compiler_version %{_user_compiler_version}
%else
%define _compiler_version 6.5.0
%endif

%if "%{_compiler}" == "gnu"
	%define _compiler_desc gcc-%{_compiler_version}
	%define _cc "mpicc" 
	%define _cxx "mpicxx"
	%define _f77 "mpif77"
	%define _fc "mpif90"
%endif

%if "%{_compiler}" == "intel"
	%define _compiler_desc intel-2013
	%define _cc icc
	%define _cxx icpc
	%define _f77 ifort
	%define _fc ifort
%endif

%if "%{_compiler}" == "pgi"
	%define _compiler_desc pgi-18.10
	%define _cc pgcc
	%define _cpp cpp
	%define _cxx pgc++
	%define _f77 pgf77
	%define _fc pgf90
	%define _ldflags ""
%endif


%define _install_path /opt/tools/libraries/netcdf/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/netcdf-%{_version}-%{_compiler_desc}

Name:           anm-netcdf
Version:        %{_version}
Release:        %{_compiler_version}.2%{?dist}
Summary:        anm-netcdf-full
BuildRequires:  curl-devel
BuildRequires:  zlib-devel >= 1.2.5
BuildRequires:  m4
Requires:       anm-hdf5
Requires:		anm-openmpi
AutoReqProv:    no


Group:          Miscellanous
License:        GPL
Source0:        ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.1.3.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
anm-netcdf-full

%prep
%setup -q -n netcdf-%{_version}

%build

export CPPFLAGS="-I$hdf5_INC"
export LDFLAGS="-L$hdf5_LIB -lhdf5 -lhdf5_hl"
export CFLAGS="-I$hdf5_INC"

./configure --prefix=%{_install_path} \
    --enable-shared \
	--enable-fortran \
	--enable-parallel \
    --enable-dap \
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
%{_module_path}
%{_install_path}
