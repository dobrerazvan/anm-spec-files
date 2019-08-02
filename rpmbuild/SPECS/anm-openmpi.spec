%define _name openmpi
%define _version 3.1.1
%define _compiler gnu
%define _compiler_version 6.5.0

%if "%{_compiler}" == "gnu"
    %define _compiler_desc gcc-%{_compiler_version}
    %define _cc "gcc" 
    %define _cxx "c++"
    %define _f77 "gfortran"
    %define _fc "gfortran"
    %define _ldflags ""
%endif

%if "%{_compiler}" == "intel"
    %define _compiler_desc intel-2015
    %define _cc icc
    %define _cxx icpc
    %define _f77 ifort
    %define _fc ifort
    %define _ldflags "-lirc"
%endif

%define _install_path /opt/tools/libraries/openmpi/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/openmpi-%{_version}-%{_compiler_desc}

Name:           anm-openmpi
Version:        %{_version}
Release:        %{_compiler_version}.1.%{?dist}
Summary:        anm-openmpi
BuildRequires:  libxml2-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  postfix
BuildRequires:  opensm
BuildRequires:  opensm-devel
BuildRequires:  numactl
BuildRequires:  hwloc-devel
#BuildRequires:  slurm-devel
BuildRequires:  rdma-core-devel
Requires:       libxml2
Requires:       environment-modules
AutoReqProv:    no


Group:          Miscellanous
License:        GPL
Source0:        http://www.open-mpi.org/software/ompi/v3.1/downloads/openmpi-%{_version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
anm-openmpi

%prep
%setup -q -n openmpi-%{_version}

%build
export CC=%{_cc} 
export CXX=${_cxx} 
export F77=%{_f77} 
export FC=%{_fc}
export LDFLAGS=%{_ldflags}

./configure --prefix=%{_install_path} \
    --enable-shared \
    --enable-mpi-fortran \
    --with-verbs \
    --disable-static \
    --enable-builtin-atomics \
    --with-slurm
make clean
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
