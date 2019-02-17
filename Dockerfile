FROM centos:7
MAINTAINER Anshu Goel

RUN yum -y install epel-release &&\
yum -y install boinc-client &&\
yum -y clean all
COPY /global_prefs_override.xml /
CMD boinc --attach_project ${boincurl} ${boinckey}