## START: Set by rpmautospec
## (rpmautospec version 0.8.2)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           yq
Version:        4.53.2
Release:        %autorelease
Summary:        Portable command-line YAML, JSON, XML, CSV, TOML and properties processor

License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND MIT
URL:            https://github.com/mikefarah/yq
Source0:        https://github.com/mikefarah/yq/archive/refs/tags/v%{version}.tar.gz

%global debug_package %{nil}

BuildRequires:  git
BuildRequires:  go
BuildRequires:  bash-completion
BuildRequires:  fish
BuildRequires:  zsh

%description
Yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor.

%package fish-completion
Summary:        Fish shell completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       fish

%description fish-completion
This package contains Fish shell completion for %{name}.

%package zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       zsh

%description zsh-completion
This package contains Zsh shell completion for %{name}.

%prep
%setup -q

%build
export GO111MODULE=on
export GOPROXY=https://proxy.golang.org,direct

go build -mod=mod -o %{name} .

./%{name} shell-completion bash > %{name}.bash
./%{name} shell-completion fish > %{name}.fish
./%{name} shell-completion zsh  > %{name}.zsh

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

install -Dpm 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -Dpm 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -Dpm 0644 %{name}.zsh  %{buildroot}%{zsh_completions_dir}/_%{name}

%check
export GO111MODULE=on
export GOPROXY=https://proxy.golang.org,direct

go test -mod=mod -o %{name} .

%files
%license LICENSE
%doc README.md
%{_bindir}/yq
%{bash_completions_dir}/%{name}

%files fish-completion
%{fish_completions_dir}/%{name}.fish

%files zsh-completion
%{zsh_completions_dir}/_%{name}

%changelog
* Fri Apr 17 2026 - Danie de Jager <danie.dejager@gmail.com> - 4.53.2-1 
* Thu Mar 2026 Danie de Jager <danie.dejager@gmail.com> - 4.52.5-1
- Fix: reset TOML decoder state between files (#2634) thanks @terminalchai
- Fix: preserve original filename when using --front-matter (#2613) thanks @cobyfrombrooklyn-bot
- Fix typo in filename (#2611) thanks @alexandear
- Bumped dependencies
* Sat Mar 7 2026 Danie de Jager <danie.dejager@gmail.com> - 4.52.4-1
* Tue Jan 13 2026 Danie de Jager <danie.dejager@gmail.com> - 4.50.1-1
* Sun Sep 14 2025 Danie de Jager <danie.dejager@gmail.com> - 4.47.2-1
- Initial AL2023 build without go-vendor-tools
- Split fish and zsh completions into subpackages

