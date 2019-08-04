%define _name netcdf
%define _version 4.6.3
%define _compiler gnu
%define _compiler_version 6.5.0

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
Release:        %{_compiler_version}.1%{?dist}
Summary:        anm-netcdf-c
BuildRequires:  curl-devel
BuildRequires:  zlib-devel >= 1.2.5
BuildRequires:  m4
Requires:       anm-hdf5
AutoReqProv:    no


Group:          Miscellanous
License:        GPL
Source0:        https://github.com/Unidata/netcdf-c/archive/v%{_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
anm-netcdf-c

%prep
%setup -q -n netcdf-c-%{_version}

%build

module load anm-hcdf5-1.10.5-gcc-6.5.0
export CPPFLAGS="-I$hdf5_INC"
export LDFLAGS="-L$hdf5_LIB"
export CFLAGS="-L$hdf5_LIB -I$hdf5_INC"
export CC=mpicc


export CC=%{_cc} 
export CXX=${_cxx} 
export F77=%{_f77} 
export FC=%{_fc}

./configure --prefix=%{_install_path} \
    --enable-shared \
    --enable-netcdf-4 \
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

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_module_path}
%{_install_path}
