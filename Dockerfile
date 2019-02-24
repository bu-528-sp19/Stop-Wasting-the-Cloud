FROM centos:7
MAINTAINER Anshu Goel


RUN yum -y install epel-release &&\
yum -y install boinc-client &&\
yum -y clean all
RUN chgrp -R 0 /var/lib/boinc && \
chmod -R g=u /var/lib/boinc
WORKDIR /var/lib/boinc

CMD boinc --attach_project ${boincurl} ${boinckey} --allow_multiple_clients --allow_remote_gui_rpc

