FROM centos:7
MAINTAINER Jhukhirtha

RUN yum -y install epel-release &&\
yum -y install boinc-client &&\
yum -y clean all
RUN chgrp -R 0 /var/lib/boinc && \
chmod -R g=u /var/lib/boinc
WORKDIR /var/lib/boinc
COPY /cgroup.py /var/lib/boinc

ENV boincurl http://www.worldcommunitygrid.org 
ENV boinckey 	3d9a693f5a8802fabaf667dc32610bae
CMD python cgroup.py && boinc --attach_project ${boincurl} ${boinckey} --allow_multiple_clients  --allow_remote_gui_rpc

