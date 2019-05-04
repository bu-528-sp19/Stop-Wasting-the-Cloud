This folder contains the different dockerfiles needed to test our project


There are three different configurations that can be tested

1) Dockerfile_baseimage: This will build the orignal BOINC without any modification
To use this, copy this file in the root folder and rename it "Dockerfile"

2) Dockerfile_withCgroup: This will build the orignal BOINC while passing Cgroup limit to configuration file of BOINC
To use this, copy cgroup.py and Dockerfile_withCgroup (rename it "Dockerfile") in the root folder

3) Dockerfile_newBOINC: This replaces the binaries of orignal BOINC and builds BOINC with our version
To use this, copy cgroup.py, boinc and Dockerfile_newBOINC (rename it "Dockerfile") in the root folder

 You can build it in two ways

Locally:
`docker login`

`docker build -t <dockerhub_userid>/<imagename> .`

`docker push <dockerhub_userid>/<imagename>`

On Docker Hub:
Set up a autobuild linking to this github repo. Each time there is a change in the github repo (i.e when you paste the desired Dockerfile in the root directory), Docker will automatically build an image. 

In the deployment yaml files, under the image tag, you will have to replace the existing image name with the one you built. 




