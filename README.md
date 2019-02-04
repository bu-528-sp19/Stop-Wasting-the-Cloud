
####  The purpose of this project is to optimize slack resources for the OpenShift clusters on the Massachusetts Open Cloud (MOC) for World Community Grid (WCG) Projects or any distributed computing application running on BOINC

### Vision and Goals Of The Project:
The goal of this project is to deploy a BOINC based CentOS image on the openshift cluster in the MOC as a daemonset. 
Define an algorithm that allows the image to scale dynamically according to the available resources on each node in the cluster. This includes allowing the image to scale out to the size of the entire node when resources are available, and to scale down to practically consume nothing when the resources are not available. 
 
### Users/Personas Of The Project:
There are two users for the project:
* **Clients of the MOC**:
These are the users who pay for nodes in the MOC and wish to consume the slack resources that they are already paying for by using the empty cycles for other computation (eg: computations for the World Community Grid)
* **MOC admins**:
These are the owners of the hardware who wish to run computations that would consume the slack resources of the clusters that are not being consumed by clients.  

### Scope and Features Of The Project:
* **What will be delivered**:
Present proof of concept to use slack resource which in future can be extended to different BOINC based applications
Container will be able to scale up/down according to the requirements of the other applications in the cluster. How the scaling will be executed 

* **What will not be delivered**:
There will be no provision to run non-BOINC based jobs
The  will run only on Openshift clusters


### Solution Concept
**Create an BOINC based CentOS image**

This image will contain the project logic and BOINC configurations that is built using Docker and deployed as a Daemonset on the Openshift Cluster in the MOC
The daemonset monitors each node to see the number of resources that are currently unused.
The unused resources are consumed by our image which uses resources to deploy BOINC based jobs (run World Community Grid computations). 

**Define logic to consume slack resources on each node**

Resources can be allocated to BOINC jobs in different ways
* Scale resources to existing jobs according to the amount available
* Create/kill instances of jobs depending upon available resources
* A combination of the above two techniques

The way the resource allocation would work will depend upon the following factors:
* The minimum resources required by each job
* The maximum resources to be allowed to a job depending upon the point of diminishing returns (with respect to performance vs resources consumed), if any

Our Container consumes the wasted space on the Openshift cluster


![alt text](https://github.com/bu-528-sp19/Stop-Wasting-the-Cloud/blob/master/Diagram%201.jpeg)

Our container scales according to the available resources on the cluster

![alt text](https://github.com/bu-528-sp19/Stop-Wasting-the-Cloud/blob/master/Diagram%20-%202.jpeg)

### Acceptance criteria
The minimum viable product includes deployment of a container image that scales the resources allocated to the BOINC job depending upon the available resources.
**Stretch goals for the project include**
Have the jobs use persistent storage in order to resume from its last state in case it gets killed
Use a Kubernetes operator to monitor the resources used by the jobs and hence scale it down to avoid getting killed


### Release Planning:
Release planning section describes how the project will deliver incremental sets of features and functions in a series of releases to completion. Identification of user stories associated with iterations that will ease/guide sprint planning sessions is encouraged. Higher level details for the first iteration is expected.
**Temporary sprints:**
* Sprint 1 : Research and learn about Kubernetes, Docker, BOINC, etc. Research and consult mentors on multiple possible scaling techniques and which of them is the most feasible/efficient.  Search for an existing CentOS image and strip it down to the essentials and start building the image we need on top of it. 
* Sprint 2 : Build the image and deploy it using Docker/Quay.io
* Sprint 3 : Define the algorithm for resource allocation and scaling
* Sprint 4 : Fine-tune the algorithm for resource allocation and scaling
* Sprint 5 : Work towards stretch goals



