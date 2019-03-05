%define major 0
%define libname	%mklibname json11 %{major}
%define devname	%mklibname -d json11

Name: json11
Version: 1.0.0
Release: 1

Summary: A tiny JSON library for C++11
License: MIT
URL: https://github.com/dropbox/%{name}
Source0: %{url}/archive/v%{version}.tar.gz

BuildRequires: ninja
BuildRequires: cmake

%description
Json11 is a tiny JSON library for C++11, providing JSON parsing
and serialization.

%package -n %{libname}
Summary: Lib files for %{name}

%description -n %{libname}
%{summary}.

%package -n %{devname}
Summary: Development files for %{name}
Requires: %{libname} = %{EVRD}

%description -n %{devname}
%{summary}.

%prep
%autosetup
mkdir -p %{_target_platform}
sed -i 's@lib/@%{_lib}/@g' CMakeLists.txt
sed -i 's@lib/@%{_lib}/@g' json11.pc.in
echo "set_property(TARGET json11 PROPERTY SOVERSION 0)" >> CMakeLists.txt

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DJSON11_BUILD_TESTS=ON \

%ninja_build

%check
pushd %{_target_platform}
    ctest --output-on-failure
popd

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/lib%{name}.so.0

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.hpp
%{_libdir}/pkgconfig/%{name}.pc
