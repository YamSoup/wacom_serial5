# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		rel	1
%define		pname	wacom_serial5
Summary:	Wacom Intuos and Intuos2 serial tablet driver
Summary(en.UTF-8):	Wacom Intuos and Intuos2 serial tablet driver
Summary(pl.UTF-8):	Sterownik dla tabletów Wacom z łączem szeregowym
Name:		%{pname}%{_alt_kernel}
Version:	1.0.0
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	https://github.com/RoaldFre/%{pname}/archive/master.tar.gz
# Source0-md5:	143ff0f096e9202653ec50830ee54e61
URL:		https://github.com/RoaldFre/wacom_serial5
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A driver for old serial Wacom protocol V tablets (Intuos and Intuos2).

%description -l en.UTF-8
A driver for old serial Wacom protocol V tablets (Intuos and Intuos2).

%description -l pl.UTF-8
Sterownik dla starego typu tabletów Wacom z łączem szeregowym
używających protokołu V (Intuos i Intuos2).

%package -n kernel%{_alt_kernel}-input-%{pname}
Summary:	Wacom Intuos and Intuos2 serial tablet driver
Summary(en.UTF-8):	Wacom Intuos and Intuos2 serial tablet driver
Summary(pl.UTF-8):	Sterownik dla tabletów Wacom z łączem szeregowym
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Suggests:	linuxconsoletools >= 1.4.4-1

%description -n kernel%{_alt_kernel}-input-%{pname}
A driver for old serial Wacom protocol V tablets (Intuos and Intuos2).

%description -n kernel%{_alt_kernel}-input-%{pname} -l en.UTF-8
A driver for old serial Wacom protocol V tablets (Intuos and Intuos2).

%description -n kernel%{_alt_kernel}-input-%{pname} -l pl.UTF-8
Sterownik dla starego typu tabletów Wacom z łączem szeregowym
używających protokołu V (Intuos i Intuos2).

%prep
%setup -q -n %{pname}-master

cat > Makefile <<'EOF'
obj-m := wacom_serial5.o
EOF

%build
%build_kernel_modules -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m %{pname} -d kernel/drivers/input/tablet

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-input-%{pname}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-input-%{pname}
%depmod %{_kernel_ver}

%files	-n kernel%{_alt_kernel}-input-%{pname}
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}/kernel/drivers/input/tablet/%{pname}*.ko*
