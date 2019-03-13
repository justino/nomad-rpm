FROM centos:centos7

RUN yum update -y
RUN yum install -y rpmdevtools mock

RUN useradd -m -d /build build

USER build

WORKDIR /build

CMD set -x \
    && spectool -g -R rpmbuild/SPECS/nomad.spec \
    && rpmbuild -ba rpmbuild/SPECS/nomad.spec
