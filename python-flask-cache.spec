#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	flask-cache
Summary:	Cache support to Flask application
Summary(pl.UTF-8):	Wsparcie dla cache w aplikacjach Flask
Name:		python-%{module}
Version:	0.13.1
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/F/Flask-Cache/Flask-Cache-%{version}.tar.gz
# Source0-md5:	ab82a9cd0844891ccdb54fbb93fd6c59
URL:		http://github.com/thadeusb/flask-cache
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cache support to Flask application

%description -l pl.UTF-8
Wsparcie dla cache w aplikacjach Flask

%package -n python3-%{module}
Summary:	Cache support to Flask application
Summary(pl.UTF-8):	Wsparcie dla cache w aplikacjach Flask
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Cache support to Flask application

%description -n python3-%{module} -l pl.UTF-8
Wsparcie dla cache w aplikacjach Flask

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n Flask-Cache-%{version}

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES README LICENSE
%{py_sitescriptdir}/flask_cache
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Flask_Cache-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES README LICENSE
%{py3_sitescriptdir}/flask_cache
%{py3_sitescriptdir}/Flask_Cache-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
