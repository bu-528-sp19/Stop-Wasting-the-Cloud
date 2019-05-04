### Documentation

- [Vision and Goals Of The Project](#vision-and-goals-of-the-project)
- [Technology Stack](#technology-stack)
- [Users/Personas Of The Project](#users/personas-of-the-project)
- [Scope](#scope)
- [Solution Concept](#solution-concept)
- [Acceptance Criteria](#acceptance-criteria)
- [Release Planning](#release-planning)
- [User Manual](#user-manual)
- [Video](#video-url)
- [Mentors](#mentors)
- [Contributors](#contributors)


### Vision and Goals Of The Project:

<p align="center">
<img src="https://github.com/Jhukhirtha/Stop-Wasting-the-Cloud/blob/master/Poc.jpeg">
</p>
Traditionally, one application was deployed in 1 host. Developers were unable to deploy multiple applications due to lack of any isolation technology. This architecture wasted large percentage of compute resource. Then came in virtual machines, which allows you to run multiple guest operating system on your host operating system. Well, this isolation technique did utilize large percentage of your compute resources but most of it was actually being utilized for setting up of VM’s. Never the less, there is some percentage of the unutilized resource here also. Now, we are quickly moving towards container environment which allows multiple application to run on host OS itself by providing the needed isolation, which means another large percentage of unutilized resources.

CCurrently, there is no open source solution which makes use of these unutilized resource and if you are not into a serverless platform, then you are probably renting out cloud space from one of the cloud providers to satisfy the application traffic during peak load. Your application around 80-90% of the time is not at its peak load so you have a lot of unutilized resources and you can put those slack resource to some work by deploying an application that generates revenue like a cryptocurrency miner or contribute to scientific research. For this project, we will be going with the latter.

####  The purpose of this project is to optimize slack resources without affecting the performance of a primary application running in your cluster.

 ### Technology Stack:
* <a href="https://massopen.cloud/">**Massachusetts Open Cloud**</a>: The MOC is a new production public cloud that is a collaborative effort between higher education, government, non-profit entities, and industry. It is based on the Open Cloud Exchange model.
* <a href="https://www.openshift.com/">**OpenShift**</a>: OpenShift is an open source container application platform by Red Hat based on top of Docker containers and the Kubernetes container cluster manager for enterprise app development and deployment.
* <a href="https://www.centos.org/">**CentOS**</a>: CentOS is an open-source Linux distribution which is similar to Red Hat Enterprise Linux (RHEL) that is widely used as a platform for different deployments.
* <a href="https://hub.docker.com/">**Docker**</a>: Docker containers wrap up the software and its dependencies into a standardized unit for software development that includes everything it needs to run: code, runtime, system tools, and libraries.
* <a href="https://boinc.berkeley.edu/">**BOINC**</a>: BOINC (Berkeley Open Infrastructure for Network Computing) is an open source middleware system which supports volunteer and grid computing. 
* <a href="https://www.worldcommunitygrid.org/discover.action">**World Community Grid (WCG)</a>:** WCG is an effort to create the world's largest public computing grid to tackle scientific research projects that benefit humanity.


### Users/Personas Of The Project:
User should be having OpenShift or Kubernetes cluster. We have specifically identified two groups of users for this project and have tried to handle their concerns:

* **Developer**:
For a developer, the most important thing is how easy an application can be deployed. As developer will not be much concerned if unutilized resource is being used or not, we have made sure our application would be easy to deploy with no burden on the developer.

* **Cluster adminstrator:**:
As an administrator, your major concerns are it should not take up the entire cluster and does not affect the performance of other primary applications running on your cluster. We have made sure, the performance of the primary application is not affected in any scenario and has been our top priority

Other than that, it can be a great area of research and interest to Open Source community since all the technology stack we have used are open source and the project itself is open source and we are open to suggestion and contribution


### Scope:

We aim to provide a solution that utilizes most of the unutilized resource of all the nodes running on OpenShift and Kubernetes cluster without affecting the performance of the primary application.

**What will be delivered**:
* A docker image of BOINC that can be deployed on Openshift clusters which will run as a daemonset to consume slack resources without affecting other applications on the cluster. 

* Examples of deployment configurations in the form of yaml files that will help users deploy our BOINC image according to their requirement. 

**What will not be delivered**:
* BOINC will not be able to scale down according to dynamic need of primary application but rather it will get suspended

* Due to unavailability of read-write many persistent volume (PV) on MOC. We will not be storing the state of BOINC i.e. if BOINC pod gets killed it will restart the computation again rather than resuming from where it got killed.

In nutshell, we have not optimized BOINC currently so that it utilizes all the unutilized resource but have made sure it will not affect the performance of primary application at any cost

**Features**:
* We aim to provide a solution that is easy to deploy and does not require separate cluster level maintenance. 

* This solution will be highly scalable and will not depend on the size of the cluster, and will work even if nodes are added and removed from the cluster.



### Solution Concept

We use BOINC to utilize wasted resource. However, BOINC was developed to run on local machines. It does not perform well when deployed in a container environment. Please find the <a href="https://github.com/BOINC/boinc/issues/3100/">issue</a> raised on BOINC community
We built a solution to extend BOINC so that it works well in a container environment and does not affect the performance of the primary application. 

<p align="center">
<img src="https://github.com/Jhukhirtha/Stop-Wasting-the-Cloud/blob/master/swc.gif">
</p>

1. Built a docker image that runs BOINC inside a container, which is based on centos
2. Deploy this docker image as a daemonset. 
We use a daemonset because it fits our use-case perfectly. A daemonset ensures that a copy of the image runs on each node in the cluster.
3. Configure BOINC’s in a way that it does not hamper the performance of other application running on the node

**How we configured BOINC :** 

* 1. Ensure BOINC takes up task according to the Cgroup: BOINC runs CPU benchmarking when it starts and requests task from BOINC server accordingly. It has various fields which can be configured. A detailed explanation can be found in the following <a href="https://boinc.berkeley.edu/wiki/PreferencesXml">link</a> 

For our MVP we configure the below fields:

a. <max_ncpus_pct>70.000000</max_ncpus_pct>

b. <vm_max_used_pct>75.000000</vm_max_used_pct>

We pass these changes to BOINC preference via python script.

Total CPU of Node: "/sys/fs/cgroup/cpu/cpu.rt_period_us" is found in this file

Cgroup cpu limit: /sys/fs/cgroup/cpu/cpu.cfs_quota_us" is found in this file

We need both because it has to be passed as percentage to BOINC preference file. We create a “global_prefs_override.xml”. BOINC overrides its default setting if it finds this file exists in the same directory where it starts. 

* 2. Changing the way BOINC sees node utilization:
On local machines, since BOINC is running on the same kernel as other applications, it can see all the running processes and utilization. Boinc calculates the process utilization for BOINC-processes and non-BOINC processes and suspends itself if the non-BOINC utilization is high. This way does not work when boinc runs inside a container because it can only see processes running inside the container. However, any process inside a container can see node-level utilization in proc/stat. We use this information to change the way BOINC calculates non-BOINC utilization.

* Our method : 
Non-boinc utilization = total node utilization - boinc utilization


To simulate existing workload (primary application) running on the cluster, we have used the Linux utility called sysbench. Sysbench runs in a <a href="https://github.com/VedantMahabaleshwarkar/SysbenchContainer">container</a> on the cluster, acting as the primary workload and BOINC's priority will be to not harm the performance of sysbench. 

### Acceptance criteria
* BOINC image that can be successfully deployed on MOC.
* Utilization of the unused resources of all the nodes in the cluster.
* Consumption of slack resources without affecting the resources of the existing workload.
* Suspend itself whenever the primary workload crosses a certain limit specified by the user.

### Release Planning:

**Sprint 1 (February 4 - 14)** 

* Research and learn about Kubernetes, Docker, BOINC, etc.
 
* Consult mentors on multiple possible scaling techniques and their feasibility and efficiency.

* Build a first draft of the container and get access to MOC 

**Sprint 2 (February 15 - 28)**

* Deploy BOINC based CentOS image as a daemonset in OpenShift cluster. 

* Research the Pros and Cons of deploying our image as a Daemonset vs using the Kubernetes scheduler. 

* Pass the World Community Grid credentials to the BOINC image as secrets on Openshift instead of hard-coding them in the image. 

* Assign Persistent Volumes to pods. (This was put on hold as Openshift assigns one Persistent Volume per Daemonset while we want one Persistent Volume per pod.)

**Sprint 3 (March 1 - 21)**

* Research Quality of Service tiers. 

* Implement a start-up script to extract the cgroup memory limits enforced on the container and communicate the values to BOINC so that it does not exceed memory consumption beyond the memory limits. 

* Deploy Daemonset on various configurations across Qos tiers and benchmark results to understand which QoS should be used for the deployment of our project. 

**Sprint 4 (March 22 - April 4)**

* Come to a conclusion as to which Qos tier works best, and deploy all future tests on that QoS tier.

* Deploy non-boinc jobs to simulate primary applications on the cluster which will contend for resources. 

* Deploy non-boinc jobs in a manner that we can understand if our boinc jobs are affecting the way the non-boinc jobs perform.


**Sprint 5 (April 5 - 18)**

* Make changes in BOINC's source code so that it successfully reads the non-BOINC utilization on the node and suspends accordingly. 

#### User Manual

Please follow the instructions in the readme of <a href="https://github.com/bu-528-sp19/Stop-Wasting-the-Cloud/tree/master/Deployments">Deployment</a> folder

### <a href"https://drive.google.com/open?id=1WmiXNbAsgxovmhsvIOMmb0FYRcSRYj9U">Video URL</a>

Please find the video URL explaining the project in detail. Please download

### Mentors:
* <a href="https://www.linkedin.com/in/daniel-mcpherson-46887912/">Daniel McPherson</a>
* <a href="https://www.linkedin.com/in/patrick-dillon/">Patrick Dillon</a>

### Contributors:
* <a href="https://www.linkedin.com/in/anshu-goel-914626113/">Anshu Goel</a>
* <a href="https://www.linkedin.com/in/jhukhirtha-marhi/">Jhukhirtha Marhi Arokiasamy</a>
* <a href="https://www.linkedin.com/in/sahil-gupta1993/">Sahil Gupta</a>
* <a href="https://www.linkedin.com/in/siddharth-bakshi/">Siddharth Bakshi</a>
* <a href="https://www.linkedin.com/in/vedantmahabaleshwarkar/">Vedant Mahabaleshwarkar</a>


