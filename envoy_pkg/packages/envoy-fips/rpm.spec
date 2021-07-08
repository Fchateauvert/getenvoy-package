Name: getenvoy-envoy
# Version and release will be overwritten with pkg_rpm
Version: 0.0.1
Release: 0
License: ASL 2.0
Summary: Certified, Compliant and Conformant Builds of Envoy
URL: https://getenvoy.io
AutoReqProv : no

%define __requires_exclude libc.so.6

%description
Certified, Compliant and Conformant Builds of Envoy

%build
cat > envoy.sh <<EOF
#!/usr/bin/bash
LD_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH
EOF

%install
tar -xvf {rpm-data.tar} -C %{buildroot}
mkdir -p %{buildroot}/etc/profile.d/
install -m644 envoy.sh %{buildroot}/etc/profile.d/envoy.sh

# DO NOT REMOVE: this is to prevent rpmbuild stripping binary, which will break envoy binary
%global __os_install_post %{nil}

%files
/usr/bin/**
/opt/getenvoy/**
/etc/profile.d/envoy.sh

%post
curl -sSL http://storage.googleapis.com/getenvoy-package/clang-toolchain/0e9d364b7199f3aaecbaf914cea3d9df4e97b850/clang+llvm-9.0.0-x86_64-linux-centos7.tar.xz | \
  tar Jx --strip-components=1 -C /usr/local
