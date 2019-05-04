#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 18:51:56 2019

@author: anshugoel
"""
#min(.8, log((40/10) + 1.4)) * 10 = min (.8, log 5.4) * 10 = 7.3 cores
#min(.8, log((cgroup_%_of_cpus/10) + 1.4)) * total_cpus_of_machines
import math
filename_cgroup = "/sys/fs/cgroup/memory/memory.limit_in_bytes"
filename_all="/proc/meminfo"
cpu_quota="/sys/fs/cgroup/cpu/cpu.cfs_quota_us"
total_cpu="/sys/fs/cgroup/cpu/cpu.rt_period_us"
with open(filename_all) as f:
    for i in f:
        sline=i.split()
        if (sline[0]=='MemTotal:'):
            total_memory=sline[1]
            break


with open(filename_cgroup) as f:
    content = f.readlines()
 
for line in content:
    memory=line
percent=((int(memory)*0.001)/int(total_memory))*100


with open(cpu_quota) as f:
    content = f.readlines()
 
for line in content:
    cpu=line
    break
with open(total_cpu) as f:
    content = f.readlines()
 
for line in content:
    total=line
    break
print(int(cpu),total)
cpu_limit_percent=(((int(cpu)*100))/int(total))
print(cpu_limit_percent)
total_cores=int(total)/100000
cpu_limit_percent=min(.8,math.log((cpu_limit_percent/total_cores)+1.4,10))*total_cores
cpu_limit_percent=(cpu_limit_percent/total_cores)*100

#f = open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us', 'w')
#pickle.dump(s,f)
#f.write(str(cpu_limit_percent*10000))
#f.close()
print(cpu_limit_percent)
#cpu_limit_percent=min(cpu_limit_percent,80)
#cpu_limit_percent=50

#print(percent,int(memory)*math.exp(-6),int(total_memory))
xml_file='''<global_preferences>
  <run_on_batteries>0</run_on_batteries>
  <run_if_user_active>1</run_if_user_active>
  <run_gpu_if_user_active>0</run_gpu_if_user_active>
  <suspend_cpu_usage>50.000000</suspend_cpu_usage>
  <start_hour>0.000000</start_hour>
  <end_hour>0.000000</end_hour>
  <net_start_hour>0.000000</net_start_hour>
  <net_end_hour>0.000000</net_end_hour>
  <leave_apps_in_memory>0</leave_apps_in_memory>
  <confirm_before_connecting>0</confirm_before_connecting>
  <hangup_if_dialed>0</hangup_if_dialed>
  <dont_verify_images>0</dont_verify_images>
  <work_buf_min_days>0.100000</work_buf_min_days>
  <work_buf_additional_days>0.000000</work_buf_additional_days>
  <max_ncpus_pct>'''+str(cpu_limit_percent)+'''</max_ncpus_pct>
  <cpu_scheduling_period_minutes>60.000000</cpu_scheduling_period_minutes>
  <disk_interval>60.000000</disk_interval>
  <disk_max_used_gb>100.000000</disk_max_used_gb>
  <disk_max_used_pct>100.000000</disk_max_used_pct>
  <disk_min_free_gb>0.100000</disk_min_free_gb>
  <vm_max_used_pct>75.000000</vm_max_used_pct>
  <ram_max_used_busy_pct>'''+str(percent)+'''</ram_max_used_busy_pct>
  <ram_max_used_idle_pct>100.000000</ram_max_used_idle_pct>
  <max_bytes_sec_up>0.000000</max_bytes_sec_up>
  <max_bytes_sec_down>0.000000</max_bytes_sec_down>
  <cpu_usage_limit>100.000000</cpu_usage_limit>
  <daily_xfer_limit_mb>0.000000</daily_xfer_limit_mb>
  <daily_xfer_period_days>0</daily_xfer_period_days>
  <day_prefs> ]
     <day_of_week>0</day_of_week>
     <start_hour>0.00</start_hour>
     <end_hour>24.00</end_hour>
     <net_start_hour>0.00</net_start_hour>
     <net_end_hour>6.00</net_end_hour>
  </day_prefs> ]
  <day_prefs> ]
     <day_of_week>6</day_of_week>
     <start_hour>0.00</start_hour>
     <end_hour>24.00</end_hour>
  </day_prefs>
</global_preferences>'''
f=open("global_prefs_override.xml","w+")
f.write(xml_file)
f.close()
