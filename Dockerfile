FROM centos:7
MAINTAINER Anshu Goel

RUN yum -y install epel-release &&\
yum -y install boinc-client &&\
yum -y clean all

CMD boinc --attach_project ${boincurl} ${boinckey}