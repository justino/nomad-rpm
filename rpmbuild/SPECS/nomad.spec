%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      0.8.7
%endif

Name:           nomad
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Nomad is an open source scheduler that uses a declarative job file for scheduling virtualized, containerized, and standalone applications.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            https://www.nomadproject.io
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:        %{name}.service
Source2:        %{name}.sysconfig
Source3:        %{name}.json

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(pre):  shadow-utils
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%else
Requires:       logrotate
%endif

%description
Nomad is a single binary that schedules applications and services on Linux, Windows, and Mac.
It is an open source scheduler that uses a declarative job file for scheduling virtualized, containerized, and standalone applications.

Nomad provides several key features:
 - Declare Jobs - Users compose and submit high-level job files. Nomad handles the scheduling and upgrading of the applications over time. This flexibility makes it easy to deploy one container, dozens of containers, or even millions.
 - Plan Changes - With built-in dry-run execution, Nomad shows what scheduling decisions it will take before it takes them. Operators can approve or deny these changes to create a safe and reproducible workflow.
 - Run Apllications - Nomad runs applications and ensures they keep running in failure scenarios. In addition to long-running services, Nomad can schedule batch jobs, distributed cron jobs, and parameterized jobs.
 - Monitor Progress - Stream logs, send signals, and interact with the file system of scheduled applications. These operator-friendly commands bring the familiar debugging tools to a scheduled world.

%prep
%setup -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp nomad %{buildroot}/%{_bindir}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE1} %{buildroot}/%{_unitdir}/
%endif

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}.d
cp %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}.d/nomad.json.example

mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%pre
getent group nomad >/dev/null || groupadd -r nomad
getent passwd nomad >/dev/null || \
    useradd -r -g nomad -d /var/lib/nomad -s /sbin/nologin \
    -c "nomadproject.io user" nomad
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(755, root, root) %{_sysconfdir}/%{name}.d
%dir %attr(750, nomad, nomad) %{_sharedstatedir}/%{name}

%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755, root, root) %{_bindir}/%{name}
%attr(644, root, root) %{_sysconfdir}/%{name}.d/nomad.json.example
%attr(644, root, root) %{_sysconfdir}/sysconfig/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif

%doc

%changelog
* Wed Mar 13 2019 Justin La Sotten <justin.lasotten@gmail.com>
- Initial Build for version 0.8.7
