%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_openstack_simplify
%global foreman_dir %{?_scl_root}/usr/share/foreman
%global foreman_bundler_dir %{foreman_dir}/bundler.d

Summary: Plugin for Foreman that simplifies the UI for purposes of OpenStack install
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.4
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/jistr/foreman_openstack_simplify
Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix}rubygems
Requires: %{?scl_prefix}rubygem(deface)
Requires: foreman => 1.1
BuildRequires: %{?scl_prefix}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Plugin for Foreman that simplifies the UI for purposes of OpenStack install

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%{?scl:scl enable %{scl} "}
  gem unpack %{SOURCE0}
%{?scl:"}
%setup -q -D -T -n  %{gem_name}-%{version}
%{?scl:scl enable %{scl} "}
  gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
%{?scl:scl enable %{scl} "}
  gem build %{gem_name}.gemspec
%{?scl:"}

mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
  gem install -V \
          --local \
          --install-dir ./%{gem_dir} \
          --force \
          --rdoc \
          %{gem_name}-%{version}.gem
%{?scl:"}


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{foreman_bundler_dir}
cp -a .%{gem_instdir}/install/foreman_openstack_simplify.rb %{buildroot}%{foreman_bundler_dir}/

%clean
rm -rf %{buildroot}

%post
cd %{foreman_dir}
if [[ ! -e Gemfile.in ]]; then
  rm -f Gemfile.lock
  %{?scl:scl enable %{scl} "}
    /usr/bin/bundle install --local 1>/dev/null 2>&1
  %{?scl:"}
fi

%postun
cd %{foreman_dir}
if [[ ! -e Gemfile.in ]]; then
  rm -f Gemfile.lock
  %{?scl:scl enable %{scl} "}
    /usr/bin/bundle install --local 1>/dev/null 2>&1
  %{?scl:"}
fi

%files
%{gem_instdir}
%{gem_spec}
%{foreman_bundler_dir}/%{gem_name}.rb
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}

%changelog
* Wed Aug 7 2013 Pádraig Brady <pbrady@redhat.com> 0.0.5-2
- Depend on upstream foreman packages

* Wed Jun 5 2013 Jiri Stransky <jistr@redhat.com> 0.0.5-1
- Update gem version.

* Thu May 24 2013 Jiri Stransky <jistr@redhat.com> 0.0.4-3
- Fix post and postun scripts to use SCL where necessary.
- Make the post and postun scripts agnostic to usage of
  Bundler vs. bundler_ext.

* Wed May 22 2013 Lon Hohberger <lhh@redhat.com> 0.0.4-2
- Fix install Requires: dependency for SCL

* Mon May 20 2013 Jiri Stransky <jistr@redhat.com> 0.0.4-1
- Moved foreman_openstack_simplify.rb (for Foreman's bundler.d) into
  the gem itself, instead having it as separate source.

* Wed May 15 2013 Jiri Stransky <jistr@redhat.com> 0.0.3-2
- SCL

* Tue May 7 2013 Jiri Stransky <jistr@redhat.com> 0.0.1-1
- Initial package
