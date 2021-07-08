# getenvoy-package

**GetEnvoy is spread across multiple repos. For more details head over to [GetEnvoy.io](https://getenvoy.io/github).**

This repository contains scripts for building [Envoy Proxy](https://www.envoyproxy.io/) for [GetEnvoy](https://www.getenvoy.io/).

# Directory Structure

- [`envoy_pkg`](envoy_pkg/) contains the scripts that packages GetEnvoy with bazel configurations for GetEnvoy.
It also include packaging tests and build targets for rpm/deb/tar/docker.
- [`common`](common/) contains the `Makefile` that pulls upstream build image scripts and some modifications.
- `centos`, `ubuntu-xenial`, `alpine`and `mac` contains OS specific scripts.

# Build Image

The build image is a docker image contains all toolchains required to build Envoy, with some OS specific configuration and patches.
This is based on Envoy's [build_container](https://github.com/envoyproxy/envoy/tree/master/ci/build_container) scripts,
and it is to provide consistent build result with the combination of build image and upstream commit.

To build the image, run:
```
$ make
```

builds docker images for Linux distributions in Linux, and macOS build context in macOS.
The docker images will be tagged as `gcr.io/getenvoy-package/build-<DISTRIBUTION>:<GIT_SHA>`.

CI built images are published to [`gcr.io/getenvoy-package`](https://gcr.io/getenvoy-package).

# Build GetEnvoy package

To build the GetEnvoy package with the build image, run:

```
docker run -v ${OUTPUT_DIR}:/tmp/getenvoy-package gcr.io/getenvoy-package/build-<DISTRIBUTION>:<GIT_SHA> ./package_envoy.py --dist <DISTRIBUTION> --artifacts_directory /tmp/getenvoy-package
```

Then the tar package will be copied to where `OUTPUT_DIR` points to. The GetEnvoy package is versioned with upstream git SHA and the build repo SHA.

## Build GetEnvoy FIPS packages

This repo is capable of building a FIPS Compliant Envoy as long as the commands are run on a host running the Linux Kernel version 4.X or 5.X.  This build will work on earlier versions of the Kernel, but the resulting executable will not be compliant with the Boring Crypto certification document.

Until the upstream RBE environment is configured, you will need to setup a build host first.  16 cores, 64 gigs of ram and 250 gigs of space are recommended.  Additionally, you will need the following applications running on your host:

- git224
- Bazel
- Docker
- Patch
- Docker local registry

The first thing you will need to do is build images locally using `make`.  Then push the build images to your local registry and tag them with `latest`.  This step will be necessary until the build container is published to the GCP project.

Once the above has been done, you can build Envoy FIPS by using the following command:
```
sudo -E ./envoy_pkg/package_envoy.py --variant envoy-fips --dist linux-glibc-fips-docker --artifacts_directory /tmp/getenvoy-package --envoy_commit=d362e791eb9e4efa8d87f6d878740e72dc8330ac --build_rpm_package
```

## FIPS RPM
The executables created by the steps above will create a version of Envoy that does not depend on GLIBC, making it portable between CentOS7 and Ubuntu.  However, it does mean that an additional library needs to be downloaded and deployed on the host machine, and the `LD_LIBRARY_PATH` variable needs to point to this library.  The RPM automatically goes through these steps and adds a scipt to /etc/profile.d to specify the LD_LIBRARY_PATH automatically.  If you wish to do it yourself, run these lines of code:
```
LD_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH
```

# Debugging package pipeline

To test your local changes to `envoy_pkg`, run:
```
$ docker run -v $(pwd):/envoy_pkg -it gcr.io/getenvoy-package/build-<DISTRIBUTION>:<GIT_SHA>
```

Then inside docker run so the script won't cleanup the build environment.
```
./package_envoy.py --dist <DISTRIBUTION> --nocleanup
```

## Supported distribution
- [Linux GLIBC](https://gcr.io/getenvoy-package/build-linux-glibc) - which supports both Ubuntu 14.04+, CentOS/RHEL 7+.
- [macOS 10.14.4 with Xcode 11.1](https://circle-macos-docs.s3.amazonaws.com/image-manifest/build-474/index.html)
- [Alpine Linux](https://gcr.io/getenvoy-package/build-alpine) (experimental, no GetEnvoy release based on this)
