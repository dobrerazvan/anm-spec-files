%define _name atlas
%define _version 3.10.3
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

Name:           anm-atlas-%_version-%_compiler_desc
Version:        %{_version}
Release:        %{_compiler_version}.1%{?dist}
Summary:        anm-atlas


Group:          Miscellanous
License:        GPL
Source0:        https://netcologne.dl.sourceforge.net/project/math-atlas/Stable/%{_version}/atlas%{_version}.tar.bz2
Source1:        http://www.netlib.org/lapack/lapack-3.8.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define _install_path /opt/tools/libraries/atlas/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/libraries/atlas-%{_version}-%{_compiler_desc}

%description
anm-openmpi

%prep
%setup -q -n ATLAS
cp ../../SOURCES/lapack-3.8.0.tar.gz .

%build
export CC=%{_cc} 
export CXX=${_cxx} 
export F77=%{_f77} 
export FC=%{_fc}

rm -rf build
mkdir build && cd build
../c    onfigure --prefix=%{_install_path} \
    --shared \
    --with-netlib-lapack-tarfile=../lapack-3.8.0.tar.gz \ 
    -b 64 -Fa alg -fPIC
make clean
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make DESTDIR=%{buildroot}%{_install_path} install

install -d -m 755 $RPM_BUILD_ROOT/etc/modulefiles/libraries/
cat > $RPM_BUILD_ROOT%{_module_path} <<EOF
#%Module1.0
prepend-path PATH               %{_install_path}/bin
prepend-path LD_LIBRARY_PATH    %{_install_path}/lib
prepend-path C_INCLUDE_PATH     %{_install_path}/include

EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_install_path}
%{_module_path}
