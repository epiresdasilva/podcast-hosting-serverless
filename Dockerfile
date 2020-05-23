FROM lambci/lambda:build-python3.7
RUN yum update -y
RUN yum install -y \
      python36 \
      python36-devel \
      python36-virtualenv \
      python34-setuptools \
      gcc \
      gcc-c++ \
      findutils \
      rsync \
      Cython \
      findutils \
      which \
      gzip \
      tar \
      man-pages \
      man \
      wget \
      make \
      zip
RUN yum install libxml2
RUN yum install libxslt
RUN pip3.7 install lxml