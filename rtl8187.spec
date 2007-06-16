#
# TODO:
# - investigate other, newer drivers on the SOURCE0 ftp
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

#
# main package.
#
%define		_rel	1
%define		_rtlname    rtl8187_linux_26.1010
Summary:	Linux driver for WLAN cards based on rtl8187
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie rtl8187
Name:		rtl8187
Version:	1.10
Release:	%{_rel}
Epoch:		0
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://61.56.86.122/cn/wlan/%{_rtlname}.zip
# Source0-md5:	c5b1c7e0c094fa943a52e1a78117308b
Patch0:		kernel-net-%{name}-2.6.20.patch
URL:		http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=24&PFid=1&Level=6&Conn=5&DownTypeID=3&GetDown=false&Downloads=true
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on rtl8187.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8187.

# kernel subpackages.

%package -n kernel%{_alt_kernel}-net-rtl8187
Summary:	Linux driver for WLAN cards based on rtl8187
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie rtl8187
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-rtl8187
This is a Linux driver for WLAN cards based on rtl8187.

%description -n kernel%{_alt_kernel}-net-rtl8187 -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8187.

%prep
%setup -q -n %{_rtlname}.0622.2006
tar xvzf drv.tar.gz
tar xvzf stack.tar.gz
%patch0 -p1

%build
%if %{with kernel}
%build_kernel_modules -C ieee80211 -m ieee80211{-rtl,_crypt-rtl,_crypt_ccmp-rtl,_crypt_tkip-rtl,_crypt_wep-rtl}
%build_kernel_modules -C beta-8187 -m r8187
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
cd ieee80211
%install_kernel_modules -d net -m ieee80211{-rtl,_crypt-rtl,_crypt_ccmp-rtl,_crypt_tkip-rtl,_crypt_wep-rtl}
cd ../beta-8187
%install_kernel_modules -d net -m r8187
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-rtl8187
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-rtl8187
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-net-rtl8187
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/net/*.ko*
%endif
