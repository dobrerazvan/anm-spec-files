%define _name openblas
%define _version 0.3.5
%define _compiler gnu
%define _compiler_version 6.5.0

%if "%{_compiler}" == "gnu"
    %define _compiler_desc gcc-%{_compiler_version}
    %define _cc "gcc -O3 -march=skylake-avx512" 
    %define _cxx "c++ -O3 -march=skylake-avx512"
    %define _f77 "gfortran -O3 -march=skylake-avx512"
    %define _fc "gfortran -O3 -march=skylake-avx512"
%endif

%if "%{_compiler}" == "intel"
    %define _compiler_desc intel-2013
    %define _cc icc
    %define _cxx icpc
    %define _f77 ifort
    %define _fc ifort
%endif

Name:           anm-%{_name}-%_version-%_compiler_desc
Version:        %{_version}
Release:        %{_compiler_version}.1%{?dist}
Summary:        anm-%{_name}


Group:          Miscellanous
License:        GPL
Source0:        https://github.com/xianyi/OpenBLAS/archive/v%{version}.tar.gz#/%{_name}-%{_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1:         openblas-libs.patch
# PATCH-FIX-UPSTREAM openblas-noexecstack.patch
Patch2:         openblas-noexecstack.patch
# PATCH-FIX-UPSTREADM fix-arm64-cpuid-return.patch
Patch3:         fix-arm64-cpuid-return.patch

%define _install_path /opt/tools/libraries/%{_name}/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/%{_name}-%{_version}-%{_compiler_desc}

%description
anm-%{_name}

%prep
%setup -q -n OpenBLAS-%{_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make TARGET=HASWELL USE_THREAD=1 PREFIX=%{buildroot}%{_install_path}

%install
make  PREFIX=%{buildroot}%{_install_path} install

# Delete info about host cpu
%ifarch %ix86 x86_64
sed -i '/#define OPENBLAS_NEEDBUNDERSCORE/,/#define OPENBLAS_VERSION/{//!d}' %{buildroot}%{_install_path}/include/openblas_config.h
%endif

# Remove buildroot
sed -i 's|%{buildroot}||g' %{buildroot}%{_install_path}/lib/cmake/openblas/OpenBLASConfig.cmake
sed -i 's|%{buildroot}||g' %{buildroot}%{_install_path}/lib/pkgconfig/openblas.pc

# Remove static lib
rm -f %{buildroot}%{_install_path}/lib/*a


install -d -m 755 $RPM_BUILD_ROOT/etc/modulefiles/libraries/
cat > $RPM_BUILD_ROOT%{_module_path} <<EOF
#%Module1.0
prepend-path PATH               %{_install_path}/bin
prepend-path LD_LIBRARY_PATH    %{_install_path}/lib
prepend-path INCLUDE            %{_install_path}/include

setenv          %{_name}_DIR        %{_install_path}
setenv          %{_name}_LIB        %{_install_path}/lib
setenv          %{_name}_INC        %{_install_path}/include

EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_install_path}
%{_module_path}
