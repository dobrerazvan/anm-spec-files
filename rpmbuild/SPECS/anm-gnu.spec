%define _version 6.5.0
%define _compiler gnu
%define _compiler_version 4.8.5

%if "%{_compiler}" == "gnu"
    %define _compiler_desc gcc-%{_compiler_version}
    %define _cc "gcc" 
    %define _cxx "c++"
    %define _cflags  "-O3"
    %define _cxxflags "-O3"
    %define _f77 "gfortran"
    %define _fc "gfortran"
    %define _f90 "gfortran"
    %define _fflags "-O3" 
    %define _cpp "gcc -E"
    %define _cxxcpp "c++ -E" 
%endif

%define debug_package %{nil}
%define _install_path /opt/tools/compilers/gnu/%{_version}-%{_compiler_desc}
%define _module_path /etc/modulefiles/compilers/gcc-%{_version}

Name:           anm-gcc
Version:        %{_version}
Release:        %{_compiler_version}.2%{?dist}
Summary:        anm-gcc
BuildRequires:  gmp-devel >= 4.2
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
Requires:       gmp >= 4.2
Requires:       mpfr
Requires:       libmpc
Requires:       environment-modules
Requires:       glibc-devel

Group:          Miscellanous
License:        GPL
Source0:        https://ftp.gnu.org/gnu/gcc/gcc-%{_version}/gcc-%{_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
anm-gcc

%prep
%setup -q -n gcc-%{_version}

%build
export CC=%{_cc}
export CXX=${_cxx}
export CFLAGS=%{_cflags}
export CXXFLAGS=%{_cxxflags}
export F77=%{_f77}
export FC=%{_fc}
export F90=%{_f90}
export FFLAGS=%{_flags}
export CPP=%{_cpp}
export CXXCPP=%{_cxxcpp}

mkdir build && cd build
../configure --prefix=%{_install_path} \
    --enable-checking=release \
    --enable-languages=c,c++,fortran \
    --disable-multilib \
    --enable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=%{buildroot}

install -d -m 755 $RPM_BUILD_ROOT/etc/modulefiles/compilers
cat > $RPM_BUILD_ROOT%{_module_path} <<EOF
#%Module1.0
prepend-path PATH               %{_install_path}/bin
prepend-path LD_LIBRARY_PATH    %{_install_path}/lib64
prepend-path INCLUDE            %{_install_path}/include
prepend-path MANPATH            %{_install_path}/share/man
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_install_path}
%{_module_path}
