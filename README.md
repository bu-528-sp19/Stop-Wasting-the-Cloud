
####  The purpose of this project is to optimize slack resources for the OpenShift clusters by executing jobs of BOINC based projects. In this project we will be developing an open source proof of concept to optimize slack resource of OpenShift Cluster running on the Massachusetts Open Cloud (MOC) which can be later extended to any public cloud having OpenShift cluster.


### Vision and Goals Of The Project:
* The goal of this project is to deploy a BOINC based CentOS image on the openshift cluster in the MOC as a daemonset. 
* Define an algorithm that allows the container to scale dynamically according to the available resources on each node in the OpenShift cluster. This includes allowing the container to scale out to the size of the entire node when resources are available, and to scale down to practically consume nothing, or get killed when the resources are not available. If the container gets killed, it will be able efficiently re-execute when resources are available again.

 
### Users/Personas Of The Project:
There are two users for the project:
* **OpenShift/Kubernetes clusters:**:
Organisations/individuals who are using Openshift or Kubernetes cluster and wish to consume the slack resources that they are already paying for by using the unused cycles for running a BOINC based application (eg: computations for the World Community Grid aka WCG).
* **Cloud server admins:**:
These are the owners of the hardware/datacenter who wish to run computations that would consume the slack resources of idle nodes that are not mapped to any clients/applications.  

### Scope and Features Of The Project:

**What will be delivered**:
* Utilizing slack resources: In here, we will develop a generic algorithm which will be able to tune OpenShift and Kubernetes clusters to run BOINC based projects on their slack resources without affecting other containers running in that cluster.
* User will not have to configure or worry about how BOINC containers are going to scale or get distributed across the nodes. Scaling of resources for BOINC container will be dynamic.

### Solution Concept

In order to utilize the slack resources within a cluster, we would be deploying a BOINC based CentOS image as a DaemonSet on OpenShift cluster. A DaemonSet essentially deploys instance(s) of the required container on selected or all the nodes (based on your configuration) of the cluster on which DaemonSet is deployed. The DaemonSet would consist of the following:
* BOINC based application as a Docker image
* Dynamic resource utilization through a script that scales the resources utilized by the instance(s) of the BOINC application

![alt text](https://github.com/bu-528-sp19/Stop-Wasting-the-Cloud/blob/master/Diagram%201.jpeg)
Slack resources being put to use to run BOINC applications

**BOINC Based Application:**

BOINC (Berkeley Open Infrastructure for Network Computing) is an open source middleware system which supports volunteer and grid computing. In our case, we will be deploying World Community Grid projects, which are based on the BOINC framework.

The application will be deployed on the cloud server as Docker containers. The container will be able to scale according to the resources available to it, which will be handled by the script in the DaemonSet. The credentials required by the application will be stored in a config file.



**Dynamic resource utilization:**

Depending upon the free space available and the requirements of the other applications within the cluster, our containers will scale accordingly in order to minimize idle system resources. This will be handled by a script that allocates resources to the BOINC application by:

* Tuning at the Kubernetes and BOINC tiers in order to scale the unused resources to the existing jobs
* Automated sizing which would enable us to create/kill instances of containers depending upon the available resources
* Allowing jobs to utilize persistent storage so that they can resume from their last state in case they get killed before completion

In order to achieve maximum utilization of the cloud server resources, the following two strategies can be employed:
* Having a single BOINC app per node that consumes all the slack resources on that node
* Having multiple BOINC apps per node that divide the slack resources on a node between themselves

Further study on the cloud infrastructure as well as the effect of performance of the application with the amount of computational resources consumed would enable us to decide which of the above two strategies would work best for our case.

The division of slack resources within instances of an application hosted on a node would depend on the following factors:
* The minimum amount of resources required by each to execute successfully
* The maximum amount of resources to be allowed to an application depending upon the point of diminishing returns (with respect to performance vs resources consumed), if any

![alt text](https://github.com/bu-528-sp19/Stop-Wasting-the-Cloud/blob/master/Diagram%20-%202.jpeg)
The containers scale according to the available slack resources on the cluster

### Acceptance criteria
The minimum viable product includes deployment of a container image that scales the resources allocated to the BOINC container depending upon the available resources.

Stretch goals for the project include:
* Use a Kubernetes operator to monitor the resources used by the containers and hence scale it down to avoid getting killed

### Release Planning:
Release planning section describes how the project will deliver incremental sets of features and functions in a series of releases to completion. Identification of user stories associated with iterations that will ease/guide sprint planning sessions is encouraged. Higher level details for the first iteration is expected.

**Temporary sprints:**

* Sprint 1 (February 4 - 14) 

Research and learn about Kubernetes, Docker, BOINC, etc.
 
Consult mentors on multiple possible scaling techniques and their feasibility and efficiency.

Build a first draft of the container and get access to MOC 
* Sprint 2 (February 15 - 28) : Deploy BOINC based CentOs image as a daemonset in OpenShift cluster
* Sprint 3 (March 1 - 21) : Define the algorithm for resource allocation and scaling.
* Sprint 4 (March 22 - April 4) : Fine-tune the algorithm for resource allocation and scaling.
* Sprint 5 (April 5 - 18): Work towards stretch goals if possible.



