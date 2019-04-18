import subprocess
import os
import time


sleep_time = 120

deployment_primaries = ["primary-70-b-60.yaml", "primary-70-no-ds.yaml", "-"]
deployment_secondaries = ["burstable-30-p-70.yaml", "burstable-60-p-70.yaml", "burstable-60-p-70.yaml"]
result = []

for i in range(len(deployment_primaries)):
    current_primary = deployment_primaries[i]
    current_secondary = deployment_secondaries[i]
    if current_primary != "-":
        create_primary = "oc create -f "+current_primary
        os.system(create_primary)
    if current_secondary != "-":
        create_secondary = "oc create -f "+current_secondary
        os.system(create_secondary)
    time.sleep(sleep_time)
    result.append(subprocess.Popen("oc logs -f " + current_primary, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
    if current_primary != "-":
        result.append(subprocess.Popen("oc logs -f " + current_primary, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
        os.system("oc delete -f" + current_primary)
    if current_secondary != "-":
        os.system("oc delete -f " + current_secondary)
