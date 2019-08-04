%define _name hdf5
%define _version 1.10.5
%define _compiler gnu
%define _compiler_version 6.5.0


%if "%{_compiler}" == "gnu"
    %define _compiler_desc gcc-%{_compiler_version}
    %define _cc "mpicc"
    %define _cxx "mpicxx"
    %define _cflags  "-O3 -fPIC"
    %define _cxxflags "-O3"
    %define _f77 "mpif77"
    %define _fc "mpif90"
    %define _f90 "mpif90"
    %define _fflags "-O3 -fPIC"
    %define _cpp "gcc -E"
    %define _cxxcpp "g++ -E"	
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
    %define _cc "mpicc"
    %define _cxx "mpic++"
    %define _f77 "mpif77"
    %define _fc "mpif90"
    %define _ldflags ""
%endif

%define _install_path /opt/tools/libraries/hdf5/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/hdf5-%{_version}-%{_compiler_desc}
Name:           anm-hdf5
Version:        %_version
Release:        %_compiler_version.2%{?dist}
Summary:        anm-hdf5
BuildRequires:  zlib-devel
AutoReqProv:    no


Group:          Miscellanous
License:        GPL
Source0:        https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/%{_name}-%{_version}/src/%{_name}-%{_version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil} 

%description
anm-hdf5

%prep
%setup -q -n hdf5-%{_version}


%build
export CC=%{_cc}
export CXX=${_cxx}
export F77=%{_f77}
export FC=%{_fc}
export CFLAGS=%{_cflags}
export FFLAGS=%{_fflags}

./configure --prefix=%{_install_path} \
    --enable-shared \
    --enable-static=no \
    --enable-fortran \
    --with-pic \
    --enable-parallel \
    --enable-fortran2003
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

setenv  %{_name}_DIR    %{_install_path}
setenv  %{_name}_LIB    %{_install_path}/lib
setenv  %{_name}_BIN    %{_install_path}/bin
setenv  %{_name}_INC    %{_install_path}/include

EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_module_path}
%{_install_path}
