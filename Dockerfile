FROM centos:latest
MAINTAINER Anshu Goel

##Install BOINC
RUN yum -y update
RUN yum -y install wget
RUN wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y localinstall http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum install -y boinc-client
#RUN export PATH=/etc/init.d/boinc-client:$PATH

##Set working directory
# WORKDIR /var/lib/boinc

##Run BOINC by default. Expects env vars for url and account key
CMD boinc start; sleep 5s; /usr/bin/boinccmd --project_attach ${boincurl} ${boinckey}; tail -f /var/boinc/std*.txt