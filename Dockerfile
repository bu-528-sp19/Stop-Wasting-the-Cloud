FROM centos:7
MAINTAINER Anshu Goel

RUN yum -y install epel-release &&\
yum -y install boinc-client &&\
#chmod +rw+rw+rw+ /var/lib/BOINC/ * . * &&\
yum -y clean all
#chmod -rw-rw-rw- / &&\

CMD boinc --attach_project ${boincurl} ${boinckey} --allow_multiple_clients --allow_remote_gui_rpc