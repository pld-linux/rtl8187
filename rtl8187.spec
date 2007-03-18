# TODO:
# - how to break lines while many modules passing?
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

#
# main package.
#
%define		_rel	0.1
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
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-net-rtl8187
This is a Linux driver for WLAN cards based on rtl8187.

%description -n kernel%{_alt_kernel}-net-rtl8187 -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8187.

%package -n kernel%{_alt_kernel}-smp-net-rtl8187
Summary:	Linux driver for WLAN cards based on rtl8187
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie rtl8187
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-net-rtl8187
This is a Linux driver for WLAN cards based on rtl8187.

%description -n kernel%{_alt_kernel}-smp-net-rtl8187 -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
rtl8187.

%prep
%setup -q -n %{_rtlname}.0622.2006
tar xvzf drv.tar.gz
tar xvzf stack.tar.gz

%build
%if %{with kernel}
%build_kernel_modules -C ieee80211 -m ieee80211-rtl,ieee80211_crypt-rtl,ieee80211_crypt_ccmp-rtl,ieee80211_crypt_tkip-rtl,ieee80211_crypt_wep-rtl
%build_kernel_modules -C beta-8187 -m r8187
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
cd ieee80211
%install_kernel_modules -m ieee80211-rtl,ieee80211_crypt-rtl,ieee80211_crypt_ccmp-rtl,ieee80211_crypt_tkip-rtl,ieee80211_crypt_wep-rtl -d net
cd ../beta-8187
%install_kernel_modules -m r8187 -d net
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-rtl8187
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-rtl8187
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-rtl8187
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-rtl8187
%depmod %{_kernel_ver}smp

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-rtl8187
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/net/*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-rtl8187
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/net/*.ko*
%endif
%endif
